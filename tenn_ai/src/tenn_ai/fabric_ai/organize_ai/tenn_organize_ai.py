
import os
import argparse
import datetime
from tabulate import tabulate

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.edrak.databases.tenn_organize_db import TENN_OrganizeDB, TENN_Tag, TENN_AwarenessTag


from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import or_
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

#########################################################################################################

class TENN_OrganizeAI():

    def __init__(self,passed_verbose: bool = False, edrakDB_path:str=False):
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()
        parser = argparse.ArgumentParser(description='none')    
        parser.add_argument('folder', type=str, help='The folder to monitor')     
        self.verbose = passed_verbose 
        self.edrakDB_path = edrakDB_path
        organize_db = TENN_OrganizeDB(edrakDB_path)
        self.engine=organize_db.connect() 

        self.unique_awareness_ids = []
    
    #################################################################################
    #################################################################################
    #################################################################################

    def create_tag(self, tag_name: str, tag_description: str, tag_parent_id: int = 0):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            # Use the create_tag method of TENN_Tag to create a new tag
            new_tag = TENN_Tag(tag_name, tag_description, tag_parent_id)
            created_tag = new_tag.create_tag(session)
            print(f"Created Tag: {created_tag.tag_name} (ID: {created_tag.tag_id})")
            session.close()
        except Exception as e:
            print(f"Error creating tag: {e}")
        return

    # #########################################################################################################

    def modify_tag(self, passed_tag_id: int, passed_tag_new_parent_id: int, passed_tag_new_description: str):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            tag_to_modify = session.query(TENN_Tag).filter(
                (TENN_Tag.tag_id == passed_tag_id) & (TENN_Tag.active == True)
            ).first()
            if tag_to_modify:
                if (
                    tag_to_modify.tag_parent_tag_id == passed_tag_new_parent_id
                    and tag_to_modify.tag_description == passed_tag_new_description
                ):
                    print(f"Tag with ID {passed_tag_id} is already modified with the same parameters.")
                else:
                    # Update the tag's parent ID and description
                    tag_to_modify.tag_parent_tag_id = passed_tag_new_parent_id
                    tag_to_modify.tag_description = passed_tag_new_description
                    # Set the updated timestamp to the current UTC time
                    tag_to_modify.updated = datetime.datetime.utcnow()
                    session.commit()
                    print(f"Modified Tag: {tag_to_modify.tag_name} (ID: {tag_to_modify.tag_id})")
            else:
                existing_tag = session.query(TENN_Tag).filter_by(tag_id=passed_tag_id).first()
                if existing_tag:
                    if existing_tag.active is False:
                        print(f"Tag with ID {passed_tag_id} is deactivated. Cannot modify a deactivated tag.")
                    else:
                        print(f"Tag with ID {passed_tag_id} not found.")
                else:
                    print(f"Tag with ID {passed_tag_id} not found.")
        except Exception as e:
            print(f"Error modifying tag: {e}")
        finally:
            session.close()

    # #########################################################################################################

    def rename_tag(self, passed_tag_id: int, new_tag_name: str):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            tag_to_rename = session.query(TENN_Tag).filter(
                (TENN_Tag.tag_id == passed_tag_id) & (TENN_Tag.active == True)
            ).first()
            if tag_to_rename:
                # Check if the new name is the same as the current name
                if tag_to_rename.tag_name == new_tag_name:
                    print(f"Tag with ID {passed_tag_id} is already named '{new_tag_name}'.")
                else:
                    # Update the tag's name
                    tag_to_rename.tag_name = new_tag_name
                    # Set the updated timestamp to the current UTC time
                    tag_to_rename.updated = datetime.datetime.utcnow()
                    session.commit()
                    print(f"Renamed Tag: {new_tag_name} (ID: {tag_to_rename.tag_id})")
            else:
                # Check if the tag exists but is deactivated
                existing_tag = session.query(TENN_Tag).filter_by(tag_id=passed_tag_id).first()
                if existing_tag:
                    if existing_tag.active is False:
                        print(f"Tag with ID {passed_tag_id} is deactivated. Cannot rename a deactivated tag.")
                    else:
                        print(f"Tag with ID {passed_tag_id} not found.")
                else:
                    print(f"Tag with ID {passed_tag_id} not found.")
        except Exception as e:
            print(f"Error renaming tag: {e}")
        finally:
            session.close()

    # #########################################################################################################
    
    def delete_tag(self, passed_tag_id: int):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            tag_to_delete = session.query(TENN_Tag).filter(
                (TENN_Tag.tag_id == passed_tag_id) & (TENN_Tag.active == True)
            ).first()
            if tag_to_delete:
                # Delete the tag
                session.delete(tag_to_delete)
                session.commit()
                print(f"Deleted Tag: {tag_to_delete.tag_name} (ID: {tag_to_delete.tag_id})")
            else:
                # Check if the tag exists but is deactivated
                existing_tag = session.query(TENN_Tag).filter_by(tag_id=passed_tag_id).first()
                if existing_tag:
                    if existing_tag.active is False:
                        print(f"Tag with ID {passed_tag_id} is deactivated. Cannot delete a deactivated tag.")
                    else:
                        print(f"Tag with ID {passed_tag_id} not found.")
                else:
                    print(f"Tag with ID {passed_tag_id} not found.")
        except Exception as e:
            print(f"Error deleting tag: {e}")
        finally:
            session.close()

    # #########################################################################################################

    def move_tag(self, passed_tag_id: int, passed_tag_new_parent_id: int):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            tag_to_move = session.query(TENN_Tag).filter(
                (TENN_Tag.tag_id == passed_tag_id) & (TENN_Tag.active == True)
            ).first()
            if tag_to_move:
                # Update the tag's parent ID
                tag_to_move.tag_parent_tag_id = passed_tag_new_parent_id
                # Set the updated timestamp to the current UTC time
                tag_to_move.updated = datetime.datetime.utcnow()
                session.commit()
                print(f"Moved Tag: {tag_to_move.tag_name} (ID: {tag_to_move.tag_id}) to Parent ID: {passed_tag_new_parent_id}")
            else:
                # Check if the tag exists but is deactivated
                existing_tag = session.query(TENN_Tag).filter_by(tag_id=passed_tag_id).first()
                if existing_tag:
                    if existing_tag.active is False:
                        print(f"Tag with ID {passed_tag_id} is deactivated. Cannot move a deactivated tag.")
                    else:
                        print(f"Tag with ID {passed_tag_id} not found.")
                else:
                    print(f"Tag with ID {passed_tag_id} not found.")
        except Exception as e:
            print(f"Error moving tag: {e}")
        finally:
            session.close()

    # #########################################################################################################

    def deactivate_tag(self, tag_id: int):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            # Find the tag by ID
            tag_to_deactivate = session.query(TENN_Tag).filter_by(tag_id=tag_id).first()
            if tag_to_deactivate:
                # Deactivate the tag by setting the "active" flag to False
                tag_to_deactivate.active = False
                session.commit()
                print(f"Deactivated Tag: {tag_to_deactivate.tag_name} (ID: {tag_to_deactivate.tag_id})")
            else:
                print(f"Tag with ID {tag_id} not found.")
            session.close()
        except Exception as e:
            print(f"Error deactivating tag: {e}")

    # #########################################################################################################

    def reactivate_tag(self, tag_id: int):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            tag_to_reactivate = session.query(TENN_Tag).filter(
                (TENN_Tag.tag_id == tag_id) & (TENN_Tag.active == False)
            ).first()
            if tag_to_reactivate:
                # Reactivate the tag by setting the "active" flag to True
                tag_to_reactivate.active = True
                session.commit()
                print(f"Reactivated Tag: {tag_to_reactivate.tag_name} (ID: {tag_to_reactivate.tag_id})")
            else:
                # Check if the tag exists but is already active
                existing_tag = session.query(TENN_Tag).filter_by(tag_id=tag_id).first()
                if existing_tag:
                    if existing_tag.active is True:
                        print(f"Tag with ID {tag_id} is already active.")
                    else:
                        print(f"Tag with ID {tag_id} not found.")
                else:
                    print(f"Tag with ID {tag_id} not found.")
            session.close()
        except Exception as e:
            print(f"Error reactivating tag: {e}")

    # #########################################################################################################

    def describe_tag(self, tag_id: int):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            # Query the tag by ID, including only active tags
            tag = session.query(TENN_Tag).filter((TENN_Tag.tag_id == tag_id) & (TENN_Tag.active == True)).first()
            if tag:
                tag_info = [
                    tag.tag_id,
                    tag.tag_name,
                    tag.tag_description,
                    tag.tag_parent_tag_id,
                    tag.active,
                    tag.created,
                    tag.updated
                ]
                headers = [
                    "Tag ID",
                    "Tag Name",
                    "Tag Description",
                    "Parent Tag ID",
                    "Active",
                    "Created",
                    "Updated"
                ]
                print(f"Tag Details for ID {tag_id}:")
                print(tabulate([tag_info], headers, tablefmt="grid"))
            else:
                existing_tag = session.query(TENN_Tag).filter_by(tag_id=tag_id).first()
                if existing_tag:
                    if existing_tag.active is False:
                        print(f"Tag with ID {tag_id} is deactivated. Cannot describe a deactivated tag.")
                    else:
                        print(f"Tag with ID {tag_id} not found.")
                else:
                    print(f"Tag with ID {tag_id} not found.")
        except Exception as e:
            print(f"Error describing tag: {e}")
        finally:
            session.close()

    # #########################################################################################################

    def get_all_id(self):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            all_tags = session.query(TENN_Tag).filter(TENN_Tag.active == True).all()
            session.close()

            tag_info = []
            for tag in all_tags:
                tag_info.append({
                    'tag_id': tag.tag_id,
                    'tag_name': tag.tag_name,
                    'tag_description': tag.tag_description,
                    'tag_parent_id': tag.tag_parent_tag_id
                })
            print(tag_info)
            return tag_info
        except Exception as e:
            print(f"Error fetching all tag IDs: {e}")
            return []

    # #########################################################################################################

    def describe_tags_tree(self):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            # Query all active tags
            tags = session.query(TENN_Tag).filter_by(active=True).all()
            if tags:
                table_data = []
                for tag in tags:
                    tag_info = [
                        tag.tag_id,
                        tag.tag_name,
                        tag.tag_description,
                        tag.tag_parent_tag_id,
                        tag.active,
                        tag.created,
                        tag.updated
                    ]
                    table_data.append(tag_info)
                headers = [
                    "Tag ID",
                    "Tag Name",
                    "Tag Description",
                    "Parent Tag ID",
                    "Active",
                    "Created",
                    "Updated"
                ]
                print("All Available Active Tags:")
                print(tabulate(table_data, headers, tablefmt="grid"))
                return tabulate(table_data, headers, tablefmt="grid")
            else:
                print("No active tags found.")
                return None
        except Exception as e:
            print(f"Error describing all tags: {e}")
        finally:
            session.close()

    # #########################################################################################################

    def get_tags_tree(self):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            tags = session.query(TENN_Tag).filter_by(active=True).all()
            # A hierarchical representation of active tags
            tag_tree = {}
            for tag in tags:
                parent_id = tag.tag_parent_tag_id
                if parent_id not in tag_tree:
                    tag_tree[parent_id] = []
                tag_tree[parent_id].append(tag)
            for parent_id, children in tag_tree.items():
                print(f"Parent ID: {parent_id}")
                for child in children:
                    print(f"  Child Tag: {child.tag_name} (ID: {child.tag_id})")
            return tag_tree
        except Exception as e:
            print(f"Error getting active tags tree: {e}")
            return None
        finally:
            session.close()
        
    # #########################################################################################################

    def get_tags_count(self):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            # Count only active tags in the database
            count = session.query(TENN_Tag).filter_by(active=True).count()
            print(f"Number of Active Tags in the Database: {count}")
            return count
        except Exception as e:
            print(f"Error counting active tags: {e}")
        finally:
            session.close()

    # #########################################################################################################

    def get_tags_by_date(self, start_date: datetime, end_date: datetime):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            # Query only active tags created or updated within the date range
            tags_within_date_range = session.query(TENN_Tag).filter(
                (TENN_Tag.created >= start_date) & (TENN_Tag.created <= end_date) &
                (TENN_Tag.active == True)
            ).all()
            if tags_within_date_range:
                print("Active Tags Created/Updated within Date Range:")
                for tag in tags_within_date_range:
                    print(f"Tag Name: {tag.tag_name}, Created: {tag.created}, Updated: {tag.updated}")
            else:
                print("No active tags found within the specified date range.")
        except Exception as e:
            print(f"Error getting active tags by date range: {e}")
        finally:
            session.close()

    # #########################################################################################################

    # def assign_tags_to_aid(self, tag_ids: list, awareness_id: int):
    #     try:
    #         Session = sessionmaker(bind=self.engine)
    #         session = Session()
    #         assigned_tags = []
    #         inactive_or_deleted_tags = []
    #         for tag_id in tag_ids:
    #             # Check if the tag exists
    #             existing_tag = session.query(TENN_Tag).filter_by(tag_id=tag_id).first()
    #             if existing_tag:
    #                 # Check if the tag is active
    #                 if existing_tag.active:
    #                     # Check if the relationship already exists
    #                     existing_relationship = session.query(TENN_AwarenessTag).filter(
    #                         (TENN_AwarenessTag.tag_id == tag_id) & (TENN_AwarenessTag.awareness_id == awareness_id)
    #                     ).first()
    #                     if not existing_relationship:
    #                         relationship_instance = TENN_AwarenessTag(
    #                             tag_id=tag_id,
    #                             awareness_id=awareness_id
    #                         )
    #                         # Assign the relationship
    #                         session.add(relationship_instance)
    #                         assigned_tags.append(tag_id)
    #                     else:
    #                         print(f"Tag {tag_id} is already assigned to the awareness ID {awareness_id}")
    #                 else:
    #                     print(f"Tag {tag_id} is deactivated and can't be assigned.")
    #                     inactive_or_deleted_tags.append(tag_id)
    #             else:
    #                 print(f"Tag {tag_id} not found.")
    #                 inactive_or_deleted_tags.append(tag_id)
    #         session.commit()
    #         session.close()
    #         if assigned_tags:
    #             print("Tags assigned to awareness successfully:")
    #             for tag_id in assigned_tags:
    #                 print(f"- Tag {tag_id}")
    #     except Exception as e:
    #         print(f"Error assigning tags to awareness: {e}")

    # #########################################################################################################

    def remove_tags_from_aid(self, tag_ids: list, awareness_id: int):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            removed_tags = []
            inactive_or_deleted_tags = []
            for tag_id in tag_ids:
                # Check if the tag exists
                existing_tag = session.query(TENN_Tag).filter_by(tag_id=tag_id).first()
                if existing_tag:
                    # Check if the tag is active
                    if existing_tag.active:
                        # Check if the relationship exists
                        existing_relationship = session.query(TENN_AwarenessTag).filter(
                            (TENN_AwarenessTag.tag_id == tag_id) & (TENN_AwarenessTag.awareness_id == awareness_id)
                        ).first()
                        if existing_relationship:
                            # Remove the relationship
                            session.delete(existing_relationship)
                            removed_tags.append(tag_id)
                        else:
                            print(f"Tag {tag_id} is not assigned to the awareness ID {awareness_id}")
                    else:
                        print(f"Tag {tag_id} is deactivated and can't be removed.")
                        inactive_or_deleted_tags.append(tag_id)
                else:
                    print(f"Tag {tag_id} not found.")
                    inactive_or_deleted_tags.append(tag_id)
            session.commit()
            session.close()
            if removed_tags:
                print("Tags removed from awareness successfully:")
                for tag_id in removed_tags:
                    print(f"- Tag {tag_id}")
        except Exception as e:
            print(f"Error removing tags from awareness: {e}")
    
    # #########################################################################################################

    def get_id_by_name(self, tag_name):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            tag = session.query(TENN_Tag).filter(
                (TENN_Tag.tag_name == tag_name) & (TENN_Tag.active == True)
            ).first()
            if tag:
                session.close()
                print(f"Tag with name '{tag_name}' is {tag.tag_id}.")
                return tag.tag_id
            else:
                print(f"Tag with name '{tag_name}' not found.")
                session.close()
                return None
        except Exception as e:
            print(f"Error fetching tag by name: {e}")
            return None
        
    # #########################################################################################################

    def search(self, passed_search_string: str):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            # Perform a case-insensitive search for only active tags containing the search string
            search_results = session.query(TENN_Tag).filter(
                (TENN_Tag.active == True) & 
                (or_(
                    TENN_Tag.tag_name.ilike(f"%{passed_search_string}%"),
                    TENN_Tag.tag_description.ilike(f"%{passed_search_string}%")
                ))
            ).all()
            if search_results:
                print("Search Results:")
                for tag in search_results:
                    print(f"Tag Name: {tag.tag_name}, Description: {tag.tag_description}")
            else:
                print(f"No active results found for search string: {passed_search_string}")
        except Exception as e:
            print(f"Error searching for active tags: {e}")
        finally:
            session.close()

    # #########################################################################################################

    def get_aids_from_tags(self, passed_tag_ids: list):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            awareness_ids = []
            for tag_id in passed_tag_ids:
                # Query for relationships with the specified tag ID
                relationships = session.query(TENN_AwarenessTag).filter(
                    TENN_AwarenessTag.tag_id == tag_id
                ).all()
                # Extract awareness IDs from the relationships and add them to the list
                awareness_ids.extend([relationship.awareness_id for relationship in relationships])
            session.close()
            if not awareness_ids:
                print("There is no awareness ID in this Tag list")
            else:
                print(awareness_ids)
        except Exception as e:
            print(f"Error getting awareness IDs from tags: {e}")

    # #########################################################################################################

    def get_tags_for_aid(self, passed_aid: str):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            # Query for tags associated with the provided awareness ID
            tags_for_aid = session.query(TENN_AwarenessTag.tag_id).filter_by(awareness_id=passed_aid).all()
            session.close()
            if not tags_for_aid:
                print(f"There are no tags for awareness ID {passed_aid}")
            # Extract the tag IDs from the result and return them as a list
            print([tag[0] for tag in tags_for_aid])
        except Exception as e:
            print(f"Error getting tags for awareness ID {passed_aid}: {e}")
    
    # #########################################################################################################

    def get_inherited_tags(self, passed_aid: str, passed_include_own_tags: bool = False):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            # Query inherited tags for the specified awareness ID
            inherited_tags = session.query(TENN_Tag).join(
                TENN_AwarenessTag,
                TENN_AwarenessTag.tag_id == TENN_Tag.tag_id
            ).filter(TENN_AwarenessTag.awareness_id == passed_aid).all()
            session.close()
            if inherited_tags:
                print(f"Inherited Tags for Awareness ID {passed_aid}:")
                for tag in inherited_tags:
                    print(tag.tag_name)
                return [tag.tag_name for tag in inherited_tags]
            if passed_include_own_tags:
                own_tags = self.get_tags_for_aid(passed_aid)
                if own_tags:
                    return own_tags
            print(f"There are no inherited tags for Awareness ID {passed_aid}")
            return []
        except Exception as e:
            print(f"Error getting inherited tags for awareness ID {passed_aid}: {e}")
            return []
    
    # #########################################################################################################
    def assign_tags_to_aid(self, tag_ids: list, awareness_id: int):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            assigned_tags = []
            inactive_or_deleted_tags = []

            # Store the awareness_id in a variable
            assigned_awareness_id = awareness_id

            for tag_id in tag_ids:
                # Check if the tag exists
                existing_tag = session.query(TENN_Tag).filter_by(tag_id=tag_id).first()
                if existing_tag:
                    # Check if the tag is active
                    if existing_tag.active:
                        # Check if the relationship already exists
                        existing_relationship = session.query(TENN_AwarenessTag).filter(
                            (TENN_AwarenessTag.tag_id == tag_id) & (TENN_AwarenessTag.awareness_id == assigned_awareness_id)
                        ).first()
                        if not existing_relationship:
                            relationship_instance = TENN_AwarenessTag(
                                tag_id=tag_id,
                                awareness_id=assigned_awareness_id
                            )
                            # Assign the relationship
                            session.add(relationship_instance)
                            assigned_tags.append(tag_id)
                        else:
                            print(f"Tag {tag_id} is already assigned to the awareness ID {assigned_awareness_id}")
                    else:
                        print(f"Tag {tag_id} is deactivated and can't be assigned.")
                        inactive_or_deleted_tags.append(tag_id)
                else:
                    print(f"Tag {tag_id} not found.")
                    inactive_or_deleted_tags.append(tag_id)

            session.commit()
            session.close()

            if assigned_tags:
                print("Tags assigned to awareness successfully:")
                for tag_id in assigned_tags:
                    print(f"- Tag {tag_id}")

            # Call the recommend_tags_for_awareness function with the assigned awareness ID
            recommended_tags = self.recommend_tags_for_awareness(assigned_awareness_id, num_recommendations=2)
            print(f"Recommended tags for awareness ID {assigned_awareness_id}: {recommended_tags}")

        except Exception as e:
            print(f"Error assigning tags to awareness: {e}")
    
    #################################################################################
    #################################################################################
    #################################################################################

if __name__ == "__main__":
    organize_ai = TENN_OrganizeAI(passed_verbose=True)

    # organize_ai.create_tag("Firas_tag", "Firas is the mentor of the Project", 0)
    # organize_ai.create_tag("Joe_tag", "Joe is an AI Wizard", 1)

    # organize_ai.create_tag("Bassel_tag", "He is a Hero", 0)
    # organize_ai.create_tag("Pedro_tag", "He is a Boy", 0)
    # organize_ai.create_tag("Charbel_tag", "He is a Boy", 0)
    # organize_ai.create_tag("Caroline_tag", "She is a Girl", 1)
    # organize_ai.create_tag("Celine_tag", "She is a Girl", 1)
     
    # organize_ai.deactivate_tag(1)
    # organize_ai.deactivate_tag(3)

    # organize_ai.modify_tag(4, 2, "Pedro is an AI Wizard")
    organize_ai.rename_tag(5, "Joseph_tag")
    # organize_ai.reactivate_tag(1)
    # organize_ai.move_tag(1, 2)
    # organize_ai.delete_tag(6)

    # organize_ai.get_tags_tree()
    # organize_ai.get_tags_count()
    # organize_ai.describe_tags_tree()

    # organize_ai.get_tags_by_date(datetime.datetime(2023, 10, 1), datetime.datetime(2023, 10, 30))

    # organize_ai.search("firas")

    # organize_ai.assign_tags_to_aid([1, 3, 6, 7, 9, 2], 1)

    # organize_ai.remove_tags_from_aid([7, 6, 11, 3], 1)

    # organize_ai.get_aids_from_tags([2, 3, 6])
    # organize_ai.get_aids_from_tags([1, 3, 7])

    # organize_ai.get_tags_for_aid(1)
    # organize_ai.get_tags_for_aid(9)

    # organize_ai.get_inherited_tags(1)
    # organize_ai.get_inherited_tags(3)

    # organize_ai.recommend_tags_for_awareness(1, 2)




###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################

# API requests functions for the OrganizeAI

router_organize = APIRouter()
organizeAI = TENN_OrganizeAI()

class TagCreationInput(BaseModel):
    tag_name: str
    tag_description: str
    tag_parent_id: int = 0

class TagRenameInput(BaseModel):
    new_tag_name: str

class TagNameInput(BaseModel):
    tag_name: str

class TagIDInput(BaseModel):
    tag_id: int

# API to invoke TENN_OrganizeAI.create_tag() function from TENN_OrganizeAI UI
@router_organize.post("/create_tag")  
async def api_create_tag(data: TagCreationInput):
    try:
        organizeAI.create_tag(data.tag_name, data.tag_description, data.tag_parent_id)
        return {"Tag created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# API to invoke TENN_OrganizeAI.rename_tag() function with a tag ID
@router_organize.post("/rename_tag/{tag_id}")
async def api_rename_tag(tag_id: int, data: TagRenameInput):
    try:
        organizeAI.rename_tag(tag_id, data.new_tag_name)
        return {f"Tag with ID {tag_id} renamed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API to invoke TENN_OrganizeAI.delete_tag() function with a tag ID
@router_organize.post("/delete_tag/{tag_id}")
async def api_delete_tag(tag_id: int):
    try:
        organizeAI.delete_tag(tag_id)
        return {f"Tag with ID {tag_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API to invoke TENN_OrganizeAI.deactivate_tag() function with a tag ID
@router_organize.post("/deactivate_tag/{tag_id}")
async def api_deactivate_tag(tag_id: int):
    try:
        organizeAI.deactivate_tag(tag_id)
        return {f"Tag with ID {tag_id} deactivated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API to invoke TENN_OrganizeAI.reactivate_tag() function with a tag ID
@router_organize.post("/reactivate_tag/{tag_id}")
async def api_reactivate_tag(tag_id: int):
    try:
        organizeAI.reactivate_tag(tag_id)
        return {f"Tag with ID {tag_id} reactivated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API to invoke TENN_OrganizeAI.describe_tags_tree() function from TENN_OrganizeAI UI
@router_organize.get("/describe_tags_tree")
async def api_describe_tags_tree():
    return organizeAI.describe_tags_tree()

# # API to invoke TENN_OrganizeAI.get_all_id() function from TENN_OrganizeAI UI
# @router_organize.get("/get_all_id")
# async def api_get_all_id():
#     return organizeAI.get_all_id()

# API to invoke TENN_OrganizeAI.describe_tags_tree() function from TENN_OrganizeAI UI
@router_organize.post("/get_id_by_name")
async def api_get_id_by_name(data: TagNameInput):
    return organizeAI.get_id_by_name(data.tag_name)

# API to invoke TENN_OrganizeAI.get_tags_tree() function from TENN_OrganizeAI UI
@router_organize.get("/get_tags_tree")
async def api_get_tags_tree():
    return organizeAI.get_tags_tree()

# API to invoke TENN_OrganizeAI.get_tags_count() function from TENN_OrganizeAI UI
@router_organize.get("/get_tags_count")
async def api_get_tags_count():
    return organizeAI.get_tags_count()


