
# import fastapi and base classes
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Import TENN classes
from tenn_ai.fabric_ai.organize_ai.tenn_organize_ai import TENN_OrganizeAI

# Import the utility packages
import json
from pyxtension import Json
from pydantic import BaseModel
from typing import Optional, List
from typing import Annotated
import datetime


# API requests functions for the OrganizeAI

router_organize_ai = APIRouter()
organizeAI = TENN_OrganizeAI()

####################################################################################################
# Classes for the API requests
####################################################################################################

class TagCreationInput(BaseModel):
    tag_name: str
    tag_description: str
    tag_parent_id: int = 0

class TagNameInput(BaseModel):
    tag_name: str

# class TagModificationInput(BaseModel):
#     passed_tag_id: int
#     passed_tag_new_parent_id: int
#     passed_tag_new_description: str

class TagRenameInput(BaseModel):
    passed_tag_id: int
    new_tag_name: str

# class TagMoveInput(BaseModel):
#     passed_tag_id: int
#     passed_tag_new_parent_id: int

class TagIDInput(BaseModel):
    tag_id: int

# class TagsByDateInput(BaseModel):
#     start_date: datetime
#     end_date: datetime

# class AssignTagsInput(BaseModel):
#     tag_ids: List[int]
#     awareness_id: int

# class RemoveTagsInput(BaseModel):
#     tag_ids: List[int]
#     awareness_id: int

# class TagsForAidInput(BaseModel):
#     passed_aid: str

# class InheritedTagsInput(BaseModel):
#     passed_aid: str
#     passed_include_own_tags: bool

# class RecommendTagsInput(BaseModel):
#     awareness_id: int
#     num_recommendations: int


####################################################################################################
# Routes from tenn_api.py (merge with the routes below)
####################################################################################################


# # API to invoke TENN_OrganizeAI.create_tag() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/create_tag")
# def api_create_tag(data: TagCreationInput):
#     organizeAI.create_tag(data.tag_name, data.tag_description, data.tag_parent_id)
#     return {"status": "Tag created successfully"}

# # API to invoke TENN_OrganizeAI.modify_tag() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/modify_tag")
# def api_modify_tag(data: TagModificationInput):
#     organizeAI.modify_tag(data.passed_tag_id, data.passed_tag_new_parent_id, data.passed_tag_new_description)
#     return {"status": "Tag modified successfully"}

# # API to invoke TENN_OrganizeAI.rename_tag() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/rename_tag")
# def api_rename_tag(data: TagRenameInput):
#     organizeAI.rename_tag(data.passed_tag_id, data.new_tag_name)
#     return {"status": "Tag renamed successfully"}

# # API to invoke TENN_OrganizeAI.delete_tag() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/delete_tag")
# def api_delete_tag(data: TagIDInput):
#     organizeAI.delete_tag(data.tag_id)
#     return {"status": "Tag deleted successfully"}

# # API to invoke TENN_OrganizeAI.move_tag() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/move_tag")
# def api_move_tag(data: TagMoveInput):
#     organizeAI.move_tag(data.passed_tag_id, data.passed_tag_new_parent_id)
#     return {"status": "Tag moved successfully"}

# # API to invoke TENN_OrganizeAI.deactivate_tag() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/deactivate_tag")
# def api_deactivate_tag(data: TagIDInput):
#     organizeAI.deactivate_tag(data.tag_id)
#     return {"status": "Tag deactivated successfully"}

# # API to invoke TENN_OrganizeAI.reactivate_tag() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/reactivate_tag")
# def api_reactivate_tag(data: TagIDInput):
#     organizeAI.reactivate_tag(data.tag_id)
#     return {"status": "Tag reactivated successfully"}

# # API to invoke TENN_OrganizeAI.describe_tag() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/describe_tag")
# def api_describe_tag(data: TagIDInput):
#     organizeAI.describe_tag(data.tag_id)
#     return {"status": "Tag described successfully"}

# # API to invoke TENN_OrganizeAI.describe_tags_tree() function from TENN_OrganizeAI UI
# @router_organize_ai.get("/api/TENN_OrganizeAI/describe_tags_tree")
# def api_describe_tags_tree():
#     organizeAI.describe_tags_tree()
#     return {"status": "Tags tree described successfully"}

# # API to invoke TENN_OrganizeAI.get_tags_tree() function from TENN_OrganizeAI UI
# @router_organize_ai.get("/api/TENN_OrganizeAI/get_tags_tree")
# def api_get_tags_tree():
#     return organizeAI.get_tags_tree()

# # API to invoke TENN_OrganizeAI.get_tags_count() function from TENN_OrganizeAI UI
# @router_organize_ai.get("/api/TENN_OrganizeAI/get_tags_count")
# def api_get_tags_count():
#     organizeAI.get_tags_count()
#     return {"status": "Tag count retrieved successfully"}

# # API to invoke TENN_OrganizeAI.get_tags_by_date() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/get_tags_by_date")
# def api_get_tags_by_date(data: TagsByDateInput):
#     organizeAI.get_tags_by_date(data.start_date, data.end_date)
#     return {"status": "Tags by date retrieved successfully"}

# # API to invoke TENN_OrganizeAI.assign_tags_to_aid() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/assign_tags_to_aid")
# def assign_tags_to_aid(data: AssignTagsInput):
#     organizeAI.assign_tags_to_aid(data.tag_ids, data.awareness_id)
#     return {"status": "Tags assigned to awareness successfully."}

# # API to invoke TENN_OrganizeAI.remove_tags_from_aid() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/remove_tags_from_aid")
# def remove_tags_from_aid(data: RemoveTagsInput):
#     organizeAI.remove_tags_from_aid(data.tag_ids, data.awareness_id)
#     return {"status": "Tags removed from awareness successfully."}

# # API to invoke TENN_OrganizeAI.search_tags() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/search_tags")
# def search(passed_search_string: str):
#     organizeAI.search(passed_search_string)
#     return {"status": f"Search results for string: {passed_search_string}"}

# # API to invoke TENN_OrganizeAI.get_aids_from_tags() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/get_aids_from_tags")
# def get_aids_from_tags(passed_tag_ids: List[int]):
#     organizeAI.get_aids_from_tags(passed_tag_ids)
#     return {"status": "Retrieved awareness IDs from tags."}

# # API to invoke TENN_OrganizeAI.get_tags_for_aid() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/get_tags_for_aid")
# def get_tags_for_aid(data: TagsForAidInput):
#     organizeAI.get_tags_for_aid(data.passed_aid)
#     return {"status": f"Retrieved tags for awareness ID {data.passed_aid}"}

# # API to invoke TENN_OrganizeAI.get_inherited_tags() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/get_inherited_tags")
# def get_inherited_tags(data: InheritedTagsInput):
#     tags = organizeAI.get_inherited_tags(data.passed_aid, data.passed_include_own_tags)
#     return {"tags": tags, "status": "Inherited tags retrieved successfully."}

# # API to invoke TENN_OrganizeAI.recommend_tags_for_awareness() function from TENN_OrganizeAI UI
# @router_organize_ai.post("/api/TENN_OrganizeAI/recommend_tags_for_awareness")
# def recommend_tags_for_awareness(data: RecommendTagsInput):
#     recommended_tags = organizeAI.recommend_tags_for_awareness(data.awareness_id, data.num_recommendations)
#     return {"recommended_tags": recommended_tags, "status": "Tags recommended successfully."}




####################################################################################################
# Routes
####################################################################################################

# API to invoke TENN_OrganizeAI.create_tag() function from TENN_OrganizeAI UI
@router_organize_ai.post("/create_tag")  
async def api_create_tag(data: TagCreationInput):
    try:
        organizeAI.create_tag(data.tag_name, data.tag_description, data.tag_parent_id)
        return {"Tag created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
####################################################################################################
# API to invoke TENN_OrganizeAI.rename_tag() function with a tag ID
@router_organize_ai.post("/rename_tag/{tag_id}")
async def api_rename_tag(tag_id: int, data: TagRenameInput):
    try:
        organizeAI.rename_tag(tag_id, data.new_tag_name)
        return {f"Tag with ID {tag_id} renamed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

####################################################################################################
# API to invoke TENN_OrganizeAI.delete_tag() function with a tag ID
@router_organize_ai.post("/delete_tag/{tag_id}")
async def api_delete_tag(tag_id: int):
    try:
        organizeAI.delete_tag(tag_id)
        return {f"Tag with ID {tag_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

####################################################################################################
# API to invoke TENN_OrganizeAI.deactivate_tag() function with a tag ID
@router_organize_ai.post("/deactivate_tag/{tag_id}")
async def api_deactivate_tag(tag_id: int):
    try:
        organizeAI.deactivate_tag(tag_id)
        return {f"Tag with ID {tag_id} deactivated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

####################################################################################################
# API to invoke TENN_OrganizeAI.reactivate_tag() function with a tag ID
@router_organize_ai.post("/reactivate_tag/{tag_id}")
async def api_reactivate_tag(tag_id: int):
    try:
        organizeAI.reactivate_tag(tag_id)
        return {f"Tag with ID {tag_id} reactivated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

####################################################################################################
# API to invoke TENN_OrganizeAI.describe_tags_tree() function from TENN_OrganizeAI UI
@router_organize_ai.get("/describe_tags_tree")
async def api_describe_tags_tree():
    return organizeAI.describe_tags_tree()

####################################################################################################
# # API to invoke TENN_OrganizeAI.get_all_id() function from TENN_OrganizeAI UI
# @router_organize_ai.get("/get_all_id")
# async def api_get_all_id():
#     return organizeAI.get_all_id()

####################################################################################################
# API to invoke TENN_OrganizeAI.describe_tags_tree() function from TENN_OrganizeAI UI
@router_organize_ai.post("/get_id_by_name")
async def api_get_id_by_name(data: TagNameInput):
    return organizeAI.get_id_by_name(data.tag_name)

####################################################################################################
# API to invoke TENN_OrganizeAI.get_tags_tree() function from TENN_OrganizeAI UI
@router_organize_ai.get("/get_tags_tree")
async def api_get_tags_tree():
    return organizeAI.get_tags_tree()

####################################################################################################
# API to invoke TENN_OrganizeAI.get_tags_count() function from TENN_OrganizeAI UI
@router_organize_ai.get("/get_tags_count")
async def api_get_tags_count():
    return organizeAI.get_tags_count()


