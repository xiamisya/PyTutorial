from enum import Enum
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message", "Hello World"}


# uvicorn main:app --reload
# main: 파일 main.py (파이썬 "모듈").
# app: main.py 내부의 app = FastAPI() 줄에서 생성한 오브젝트.
# --reload: 코드 변경 후 서버 재시작. 개발에만 사용.

# http://127.0.0.1:8000 : 접속
# http://127.0.0.1:8000/docs : 자동 대화형 API 문서를 볼 수 있습니다
# http://127.0.0.1:8000/redoc : 대안 자동 문서를 볼 수 있습니다 (ReDoc 제공):

# 경로 매개 변수
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


# 경로 매개 변수 Type
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


"""
# 경로 매개 변수 순서
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
"""

"""
# 사정 정의 값
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
"""


# 경로 변환기
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

"""
# 쿼리 매개 변수(with 기본값)
# http://127.0.0.1:8000/items > http://127.0.0.1:8000/items/?skip=0&limit=10
# http://127.0.0.1:8000/items/?skip=20 >  http://127.0.0.1:8000/items/?skip=20&limit=10
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]
"""

"""
# 선택적 매개 변수
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
"""

"""
# 쿼리 매개 변수 형변환
# short에 1, True, ture, on, yes 모두 true, 0, False, false, off, no 는 false
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
"""


# 여러 경로/쿼리 매개 변수
# 특정 순서로 선언할 필요가 없습니다. 매개변수들은 이름으로 감지됩니다:
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# 필수 쿼리 매개 변수
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


"""
# 필수 쿼리 매개 변수
# (일부 매개변수는 필수로, 다른 일부는 기본값을, 또 다른 일부는 선택적으로 선언할 수 있습니다:
@app.get("/items/{item_id}")
async def read_user_item(
        item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
"""
