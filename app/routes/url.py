import validators
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from schemas import url as schemas
from models.url import UrlModel
from utils.jwt import get_current_user
from utils.random import create_random_key


router = APIRouter(
    tags=['url'],
    responses={404: {'description': 'Not found'}},
)

@router.post("/url")
def create_url(url: schemas.URLBase, user = Depends(get_current_user)) -> dict:
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400, detail="Not a valid URL")
    item = UrlModel.get_url_by_target_url(url.target_url)
    if item:
        is_url_valid = UrlModel.check_url_validity(item)
        if is_url_valid:
            return {
                "url" : f"http://localhost:8000/{item['key']}",
                "msg" : "URL already minified"
                }
        else:
            raise HTTPException(status_code=400, detail="Link expired")

    key = create_random_key()
    while UrlModel.get_original_url(key) != None:
        key = create_random_key()
    db_url = UrlModel(target_url=url.target_url, key=key).create_url()

    return {"msg": "Your URL has been created successfully", **db_url}



@router.get("/{url_key}")
def redirect_to_original_url( url_key: str):
    item = UrlModel.get_original_url(url_key)
    if item:
        is_url_valid = UrlModel.check_url_validity(item)
        if is_url_valid:
            return RedirectResponse(url=item['target_url'])
        else:
            raise HTTPException(status_code=400, detail="Link expired")
    else:
        raise HTTPException(status_code=404, detail="URL not found")
