from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Fintech Tools")


@mcp.tool()
def get_account_balance(account_id: str) -> dict:
    """Get the current balance for a given account ID"""
    accounts = {
        "ACC001": {"account_id": "ACC001", "owner": "Mahathir", "balance": 15230.50, "currency": "BDT"},
        "ACC002": {"account_id": "ACC002", "owner": "Bishal", "balance": 4820.00, "currency": "USD"},
    }
    if account_id not in accounts:
        return {"error": f"Account {account_id} not found"}
    return accounts[account_id]


@mcp.tool()
def list_transactions(account_id: str, limit: int = 5) -> list:
    """List recent transactions for a given account ID"""
    transactions = {
        "ACC001": [
            {"id": "TXN001", "amount": -500.00, "description": "Grocery", "date": "2026-09-15"},
            {"id": "TXN002", "amount": 2000.00, "description": "Salary", "date": "2026-09-14"},
            {"id": "TXN003", "amount": -150.00, "description": "Electricity bill", "date": "2026-09-13"},
        ],
        "ACC002": [
            {"id": "TXN004", "amount": -200.00, "description": "Amazon", "date": "2026-09-15"},
            {"id": "TXN005", "amount": 500.00, "description": "Freelance payment", "date": "2026-09-12"},
        ],
    }
    if account_id not in transactions:
        return [{"error": f"No transactions found for {account_id}"}]
    return transactions[account_id][:limit]


@mcp.tool()
def calculate_interest(principal: float, rate: float, years: float) -> dict:
    """Calculate simple interest. principal in currency units, rate as percentage, years as time period"""
    interest = (principal * rate * years) / 100
    return {
        "principal": principal,
        "rate_percent": rate,
        "years": years,
        "interest": round(interest, 2),
        "total": round(principal + interest, 2)
    }


if __name__ == "__main__":
    mcp.run()