from tenn_ai.fabric_ai.safe_ai.tenn_safe_db import TENN_User, TENN_Org, TENN_SafeDB

safeDB = TENN_SafeDB(passed_verbose=True)

org = TENN_Org()
org.org_id = 1
org.name = "TENN"
org.description = "TENN AI"
org.website = "https://tenn.ai"
org.main_email = "info@the.executives.network"
org.support_email = "support@the.executives.network"
org.main_phone = "+974-3315-2359"
org.address = "Tower 4, Floor 4, Workaholics, The Gate"
org.city = "Doha"
org.country = "Qatar"
org.pobox = "00001"
org.enabled = True

safeDB.add_or_update_org(org)

list_of_orgs = safeDB.get_all_orgs()

for org in list_of_orgs:
    print("org: ", str(org))

user_admin = TENN_User()
user_admin.user_id = 1
user_admin.username = "admin"
user_admin.password = "TENN"
user_admin.first_name = "TENN"
user_admin.last_name = "Admin"
user_admin.email = "digital@the.executives.network"
user_admin.mobile = "+974-3315-2359"
user_admin.city = "Doha"
user_admin.country = "Qatar"
user_admin.org_id = 1
user_admin.enabled = True

user_firas = TENN_User()
user_firas.user_id = 2
user_firas.username = "firas"
user_firas.password = "TENN"
user_firas.first_name = "Firas"
user_firas.last_name = "Sleiman"
user_firas.email = "firas.sleiman@the.executives.network"
user_firas.mobile = "+974-3372-1111"
user_firas.city = "Doha"
user_firas.country = "Qatar"
user_firas.org_id = 1
user_firas.enabled = True

safeDB.add_or_update_user(user_admin)
safeDB.add_or_update_user(user_firas)


list_of_users = safeDB.get_all_users()

for user in list_of_users:
    print("user: ", str(user))

