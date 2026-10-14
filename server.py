from mcp.server import MCPServer
from hunter_client import search_domain, find_person_email, verify_email
from typing import Annotated
from pydantic import EmailStr, Field, StringConstraints, AfterValidator

mcp = MCPServer("Hunter-IO-MCP")

Domain = Annotated[
    str,
    Field(
        min_length=4,
        max_length=253,
        pattern=r"^(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$"
    )
]
def validate_name(value: str) -> str:
    if not any(char.isalpha() for char in value):
        raise ValueError("Name must contain at least one alphabetic character")
    return value

PersonName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100
    ),
    AfterValidator(validate_name)
]

@mcp.tool()
def find_company_emails(domain: Domain) -> dict:
    """Find professional email addresses associated with a company domain."""
    val=search_domain(domain)
    return val

@mcp.tool()
def find_person_email_tool(
    first_name: PersonName,
    last_name: PersonName,
    domain: Domain
) -> dict:
    """Find a person's professional email using their name and company domain."""
    return find_person_email(first_name,last_name, domain)

@mcp.tool()
def verify_professional_email(email: EmailStr) -> dict:
    """Check an email address using Hunter.io's Email Verifier."""
    return verify_email(email)

if __name__ == "__main__":
    mcp.run()