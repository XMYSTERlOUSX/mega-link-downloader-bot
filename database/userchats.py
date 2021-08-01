from . import DB, get_stuff

AL = DB.get("ALLCHATS")
if not AL:
    DB.set("ALLCHATS", "{'USERS':[]}")

def add_chat(id: str):
    CCH = get_stuff("ALLCHATS")
    if not CCH:
        CCH.update({"USERS":[id]})
        DB.set("ALLCHATS", str(CCH))
        return
    if CCH["USERS"] and id in CCH["USERS"]:
      return
    Ul = CCH["USERS"]
    if not Ul:
      Ul = []
    Ul.append(id)
    CCH.update({"USERS":Ul})
    DB.set("ALLCHATS", str(CCH))


def get_all_chats():
    CCH = get_stuff("ALLCHATS")
    if not (CCH and CCH["USERS"]):
        return []
    return CCH["USERS"]


def remove_chat(id):
    CCH = get_stuff("ALLCHATS")
    if not CCH:
        return
    if CCH["USERS"] and id not in CCH["USERS"]:
      return
    li = CCH["USERS"]
    if id in li:
      li.remove(id)
    CCH.update({"USERS":li})
    DB.set("ALLCHATS", str(CCH))
    return True
