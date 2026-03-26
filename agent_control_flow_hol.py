import asyncio
import time
from agents import Agent, Runner, function_tool


# =========================================================
# STEP 1: SPECIALIST AGENTS
# =========================================================

billing_agent = Agent(
    name="BillingAgent",
    instructions=(
        "You are a billing support specialist.\n"
        "Handle only billing, invoices, refunds, subscription, and payment-related questions.\n"
        "Answer clearly and professionally."
    )
)

tech_agent = Agent(
    name="TechSupportAgent",
    instructions=(
        "You are a technical support specialist.\n"
        "Handle only technical issues such as login failures, app crashes, slow performance, API errors, and troubleshooting.\n"
        "Answer clearly and professionally."
    )
)

faq_agent = Agent(
    name="FAQAgent",
    instructions=(
        "You are a general FAQ assistant.\n"
        "Handle general product questions, feature explanations, and onboarding-related questions.\n"
        "Answer clearly and professionally."
    )
)


# =========================================================
# STEP 2: AGENTS-AS-TOOLS
# =========================================================
# These tools allow one main agent to call specialist agents
# like helper functions.


@function_tool
async def ask_billing_specialist(question: str) -> str:
    """
    Ask the billing specialist for help.

    Args:
        question: Billing-related customer question
    """
    result = await Runner.run(billing_agent, question)
    return result.final_output


@function_tool
async def ask_tech_specialist(question: str) -> str:
    """
    Ask the technical support specialist for help.

    Args:
        question: Technical support customer question
    """
    result = await Runner.run(tech_agent, question)
    return result.final_output


@function_tool
async def ask_faq_specialist(question: str) -> str:
    """
    Ask the FAQ specialist for help.

    Args:
        question: General FAQ customer question
    """
    result = await Runner.run(faq_agent, question)
    return result.final_output


# =========================================================
# STEP 3: HANDOFF-BASED SUPERVISOR
# =========================================================
# This supervisor TRANSFERS the user to another specialist agent.

handoff_supervisor = Agent(
    name="HandoffSupervisor",
    instructions=(
        "You are a customer support supervisor.\n"
        "Decide which specialist should handle the user's request.\n"
        "Use handoffs when the request belongs to another specialist.\n"
        "Route billing questions to BillingAgent.\n"
        "Route technical issues to TechSupportAgent.\n"
        "Route general product or FAQ questions to FAQAgent.\n"
        "If the user asks a mixed question, choose the most relevant specialist."
    ),
    handoffs=[billing_agent, tech_agent, faq_agent]
)


# =========================================================
# STEP 4: AGENTS-AS-TOOLS SUPERVISOR
# =========================================================
# This supervisor STAYS in control and CALLS specialists as tools.

tool_supervisor = Agent(
    name="ToolSupervisor",
    instructions=(
        "You are a customer support supervisor.\n"
        "You must remain the main coordinator.\n"
        "Use specialist tools whenever needed.\n"
        "Use billing specialist for billing/payment/refund issues.\n"
        "Use tech specialist for login, crash, API, or technical issues.\n"
        "Use FAQ specialist for product usage or onboarding questions.\n"
        "If the user asks a mixed question, you may call more than one specialist and combine the answer."
    ),
    tools=[ask_billing_specialist, ask_tech_specialist, ask_faq_specialist]
)


# =========================================================
# STEP 5: HIERARCHICAL AGENT
# =========================================================
# This top-level enterprise manager decides whether to:
# - use handoff supervisor
# - use tool supervisor
# - or answer directly

enterprise_manager = Agent(
    name="EnterpriseManager",
    instructions=(
        "You are the enterprise support manager.\n"
        "Your job is to choose the best control-flow strategy.\n"
        "If the user clearly needs a single specialist, use the handoff supervisor.\n"
        "If the user asks a multi-part or combined question, use the tool supervisor.\n"
        "If the question is very simple and general, answer directly if possible.\n"
        "Always provide a clean, final customer-friendly answer."
    ),
    tools=[],
    handoffs=[handoff_supervisor, tool_supervisor]
)


# =========================================================
# STEP 6: CONCURRENT EXECUTION DEMO
# =========================================================
# This function runs multiple agents at the same time.

async def concurrent_specialist_demo(question: str):
    print("\n================ CONCURRENT EXECUTION DEMO ================\n")
    print("User Question:", question)

    start_time = time.perf_counter()

    tasks = [
        Runner.run(billing_agent, question),
        Runner.run(tech_agent, question),
        Runner.run(faq_agent, question)
    ]

    results = await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print("\n--- Billing Agent Response ---")
    print(results[0].final_output)

    print("\n--- Tech Support Agent Response ---")
    print(results[1].final_output)

    print("\n--- FAQ Agent Response ---")
    print(results[2].final_output)

    print(f"\nConcurrent execution completed in {elapsed_time:.2f} seconds")
    print("\n===========================================================\n")


# =========================================================
# STEP 7: INTERACTIVE HOL MENU
# =========================================================

async def main():
    print("=" * 70)
    print(" OPENAI AGENTS SDK - AGENT CONTROL FLOW HOL ")
    print("=" * 70)
    print("\nChoose a demo mode:")
    print("1. Handoffs Demo")
    print("2. Agents-as-Tools Demo")
    print("3. Hierarchical Agent Demo")
    print("4. Concurrent Execution Demo")
    print("5. Exit")

    while True:
        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "5":
            print("Exiting HOL. Goodbye!")
            break

        user_question = input("\nEnter customer question: ").strip()

        if not user_question:
            print("Please enter a valid question.")
            continue

        start_time = time.perf_counter()

        if choice == "1":
            print("\n================ HANDOFF DEMO ================\n")
            result = await Runner.run(handoff_supervisor, user_question)
            print("Final Response:\n")
            print(result.final_output)

        elif choice == "2":
            print("\n================ AGENTS-AS-TOOLS DEMO ================\n")
            result = await Runner.run(tool_supervisor, user_question)
            print("Final Response:\n")
            print(result.final_output)

        elif choice == "3":
            print("\n================ HIERARCHICAL AGENT DEMO ================\n")
            result = await Runner.run(enterprise_manager, user_question)
            print("Final Response:\n")
            print(result.final_output)

        elif choice == "4":
            await concurrent_specialist_demo(user_question)
            continue

        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")
            continue

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        usage = result.context_wrapper.usage

        print("\n--- Metrics ---")
        print("Requests made :", usage.requests)
        print("Input tokens  :", usage.input_tokens)
        print("Output tokens :", usage.output_tokens)
        print("Total tokens  :", usage.total_tokens)
        print(f"Time taken    : {elapsed_time:.2f} sec")


if __name__ == "__main__":
    asyncio.run(main())
