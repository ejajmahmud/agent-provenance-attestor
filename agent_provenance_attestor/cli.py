"""CLI for agent-provenance-attestor."""
import sys
import argparse
from .attestor import AgentProvenanceAttestor


def main():
    parser = argparse.ArgumentParser(description="Agent Provenance Attestor")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        attestor = AgentProvenanceAttestor("audit_secret_key")
        r1 = attestor.attest_action("agent_01", "gemini-2.5-pro", "git_commit", {"sha": "c0ffee"})
        r2 = attestor.attest_action("agent_02", "claude-3.5-sonnet", "deploy_prod", {"target": "k8s"})
        print(f"Receipt 1: {r1.to_dict()}")
        print(f"Receipt 2: {r2.to_dict()}")
        print(f"Chain integrity valid: {attestor.verify_chain()}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
