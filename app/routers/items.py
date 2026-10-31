"""示例路由：内存版 CRUD，用来演示 Pydantic 校验和自动文档。

真实项目里把 _DB 换成数据库层（SQLAlchemy / SQLModel）即可。
"""

from itertools import count
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/items", tags=["items"])

# 内存存储，进程重启即清空
_DB: dict[int, "Item"] = {}
_id_seq = count(start=1)


class ItemIn(BaseModel):
    """创建/更新时提交的字段。"""

    name: str = Field(min_length=1, max_length=50, examples=["机械键盘"])
    price: float = Field(gt=0, examples=[299.0])


class Item(ItemIn):
    """返回给前端的完整对象。"""

    id: int


@router.get("", response_model=list[Item], summary="列出全部 item")
def list_items() -> list[Item]:
    return list(_DB.values())


@router.post(
    "",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="新建 item",
)
def create_item(payload: ItemIn) -> Item:
    item = Item(id=next(_id_seq), **payload.model_dump())
    _DB[item.id] = item
    return item


@router.get("/{item_id}", response_model=Item, summary="按 id 查询")
def get_item(item_id: Annotated[int, Path(ge=1, description="item 的 id")]) -> Item:
    item = _DB.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"item {item_id} 不存在"
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除")
def delete_item(item_id: int) -> None:
    if _DB.pop(item_id, None) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"item {item_id} 不存在"
        )
