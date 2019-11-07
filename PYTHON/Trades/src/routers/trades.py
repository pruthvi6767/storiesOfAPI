from fastapi import APIRouter, Body, Path, Query, HTTPException
from pydantic import BaseModel, Schema, UUID4
# from starlette.status import (
#     HTTP_200_OK,
#     HTTP_204_NO_CONTENT,
#     HTTP_422_UNPROCESSABLE_ENTITY,
#     HTTP_500_INTERNAL_SERVER_ERROR
# )
from starlette.responses import Response
from typing import List, Dict, Tuple
from uuid import uuid4
import threading
import logging
import sys
from fastapi.exceptions import RequestValidationError, ValidationError
# from concurrent.futures import ThreadPoolExecutor


logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger = logging.Logger("API")

# lock = threading.Lock()


class Trade(BaseModel):
    client_trade_id: str = Schema(
        ..., description="Unique ID for this trade that you define", max_length=256, min_length=1, example='T-50264430-bc41')
    date: int = Schema(
        ..., description="Trade date for the trade in YYYYMMDD format", ge=20010101, le=21000101, example="20200101")
    quantity: str = Schema(
        ..., description="The quantity of the trade", regex="^[-]?[0-9]*\\.?[0-9]+$", example='100')
    price: str = Schema(
        ..., description="The price of the trade", regex="^[-]?[0-9]*\\.?[0-9]+$", example='10.00')
    ticker: str = Schema(
        ..., description="Ticker (Unique Identifier) traded", example='AAPL')


class TradeSubmitted(BaseModel):
    client_trade_id: str = Schema(..., description="unique id defined by you",
                                  max_length=256, min_length=1, example='T-50264430-bc41')

    trade_id: str = Schema(..., title="",
                           description="Unique ID for this trade defined")


class InternalTrade(BaseModel):
    id: str = Schema(
        ..., description="Unique ID for this trade defined   ", max_length=256, min_length=1)
    trade: Trade


# database collections without using an embedded test (sqlite/other) database
# All Internal Trades List is collection of trade and its identity ( index of trade element in all trades List ~ database index keys as hahs table in memory) in list
# deletion marks the index like a tombstone to None and dis-advantage is those tombstone markers are never compacted as this is used for testing
all_trades: List[Trade] = [None]
all_internal_trades: List[InternalTrade] = []
all_trades_submitted: List[TradeSubmitted] = []

router = APIRouter()


@router.get("/", responses={500: {"description": "Internal Server Error"}}, response_model=List[InternalTrade], response_model_skip_defaults=True)
async def get_all_trades():
    return [all_internal_trades[i] for i in range(len(all_internal_trades)) if all_internal_trades[i] is not None]


@router.post("/", responses={400: {"description": "Bad Request - Improper Types Passed"},
                             422: {"description": "Not processable - Missing Required"},
                             500: {"description": "Internal Server Error"}
                             }, response_model=List[TradeSubmitted], response_model_skip_defaults=True, status_code=200)
def insert_trades(*, trades: List[Trade] = Body(..., embed=False), response: Response):

    if trades:
        #  synchronously
        trades_submitted = __add_to_trades(trades)

    return trades_submitted


@router.get("/{id}", response_model=InternalTrade)
async def trades_get(*, id: str = Path(..., title="Internal Trade Id", description="update trade by unique id")):
    check_if_zero(int(id))
    try:
        if all_trades[int(id)] is None:
            raise HTTPException(status_code=404, detail="ID Not Found")
        return {"id": id, "trade": all_trades[int(id)]}
    except IndexError:
        raise HTTPException(status_code=404, detail="ID Not Found")
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{id}", response_model=InternalTrade)
async def trades_update(*, id: str = Path(..., title="Internal Trade Id", description="update trade by unique id"), trade: Trade = Body(...), status_code=200):
    check_if_zero(int(id))
    try:
        if all_trades[int(id)] is None:
            raise IndexError
        old_trade = all_trades[int(id)]
        submit_index, _ = [(index, t) for index, t in enumerate(
            all_trades_submitted) if t["trade_id"] == id].pop()
        all_trades_submitted[submit_index]["client_trade_id"] = trade.client_trade_id
        # update internal trade
        int_index, _ = [(index, t) for index,
                        t in enumerate(all_internal_trades) if t["id"] == id].pop()
        all_internal_trades[int_index]["trade"] = trade
        # update trade
        all_trades[int(id)] = trade
        logger.log(logging.DEBUG,
                   " {} trade updated to {} ".format(old_trade, trade))
        logger.log(logging.INFO, "trade with id {} updated".format(id))

    except IndexError:
        raise HTTPException(status_code=404, detail="ID Not Found")
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"id": id, "trade": all_trades[int(id)]}


@router.delete("/{id}", status_code=204)
async def trades_cancel(*, id: str = Path(..., title="Internal Trade Id", description="delete trade by unique id")):
    check_if_zero(int(id))
    try:
        if all_trades[int(id)] is None:
            raise IndexError
        old_trade = all_trades[int(id)]
        print(old_trade)
        trade_submit_index, _ = [(index, t) for index, t in enumerate(
            all_trades_submitted) if t["trade_id"] == id].pop()
        all_trades_submitted[trade_submit_index] = None
        index, _ = [(index, t) for index,
                    t in enumerate(all_internal_trades) if t["id"] == id].pop()
        all_internal_trades[index] = None
        all_trades[int(id)] = None
        logger.log(logging.DEBUG,
                   " {} trade updated to {} ".format(old_trade, "None"))
        logger.log(logging.INFO, "trade with id {} updated".format(id))
        return {}
    except IndexError:
        raise HTTPException(status_code=404, detail="ID Not Found")
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")


def __add_to_trades(trades: List[Trade]) -> List[TradeSubmitted]:
    try:
        # lock.acquire()
        trades_size: int = len(all_trades)
        submit_trades_size: int = len(all_trades_submitted)
        for i, v in enumerate(trades):
            # starts from index 1 if no trades
            all_trades.append(v)

            all_trades_submitted.append(
                {"trade_id": str(trades_size+i),
                    "client_trade_id": v.client_trade_id}
            )
            all_internal_trades.append(
                {"id": str(trades_size+i), "trade": v})
    except:
        logger.log(logging.ERROR, "exception adding trades {}".format(trades))
        raise HTTPException(
            status_code=500, detail="Internal Server Error")
    # finally:
        # lock.release()
    return all_trades_submitted[submit_trades_size:]


def check_if_zero(id):
    if not id or id is None:
        raise HTTPException(status_code=404, detail="ID Not Found")
