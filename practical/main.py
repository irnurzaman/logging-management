import asyncio
import json
import sys
from typing import Optional
from structlog import get_logger

logger = get_logger()
ACCOUNTS = {"IRN": {"balance": 0.0}}

def depositAccount(acc: str, amount: float) -> Optional[str]:
    account = ACCOUNTS.get(acc)
    if not account:
        remark = "account not found"
        logger.warning(remark, method="depositAccount", acc=acc)
        return remark
    account["balance"] += amount
    logger.info("deposit success", method="depositAccount", acc=acc, amount=amount, balance=account["balance"])

def withdrawAccount(acc: str, amount: float) -> Optional[str]:
    account = ACCOUNTS.get(acc)
    if not account:
        remark = "account not found"
        logger.warning(remark, method="withdrawAccount", acc=acc)
        return remark
    if amount > account["balance"]:
        remark = "insufficient balance"
        logger.warning(remark, method="withdrawAccount", amount=amount)
        return remark
    account["balance"] -= amount
    logger.info("withdraw success", method="withdrawAccount", acc=acc, amount=amount, balance=account["balance"])

async def callback(r: asyncio.StreamReader, w: asyncio.StreamWriter):
    while not w.is_closing():
        try:
            buffer = await r.readline()
            try:
                request = json.loads(buffer.decode())
            except ValueError:
                logger.error("Parsing request to JSON error", buffer=buffer.decode())
                continue

            action = request["action"]
            if action == "deposit":
                accountNo = request["accountNo"]
                amount = request["amount"]
                logger.debug("incoming deposit request", accountNo=accountNo, amount=amount)
                remark = depositAccount(accountNo, amount)
                if remark:
                    logger.warning("deposit account failed", method="callback", accountNo=accountNo, amount=amount)
            elif action == "withdraw":
                accountNo = request["accountNo"]
                amount = request["amount"]
                logger.debug("incoming withdraw request", accountNo=accountNo, amount=amount)
                remark = withdrawAccount(accountNo, amount)
                if remark:
                    logger.warning("withdraw account failed", method="callback", accountNo=accountNo, amount=amount)
        except Exception as e:
            _, _, tb = sys.exc_info()
            logger.error("Unexpected error", method="callback", error=f"{repr(e)} | {str(e)}", line=tb.tb_lineno)
            w.close()
            return

async def main():
    server = await asyncio.start_server(callback, "localhost", 7000)
    async with server:
        await server.serve_forever()

asyncio.run(main())