from . import DB, get_stuff

AL = DB.get("BLACKLIST")
if not AL:
    DB.set("BLACKLIST", "{'USERS':[]}")


def add_blacklist(id):
    mn = get_stuff("BLACKLIST")
    try:
      lt = mn["USERS"]
    except:
      mn.update({"USERS":[id]})
      DB.set("BLACKLIST", str(mn))
      return True
    if not lt:
      lt = []
    if id not in lt:
      lt.append(id)
    mn.update({"USERS":lt})
    DB.set("BLACKLIST", str(mn))


def check_blacklist(id):
    std = get_stuff("BLACKLIST")
    try:
        MNT = std["USERS"]
    except:
        return False
    if MNT and id in MNT:
      return True
    return False


def remove_blacklist(id):
    Bl = get_stuff("BLACKLIST")
    if not (Bl and Bl["USERS"]):
        return "Blacklisted User List is Empty !"
    if id not in Bl["USERS"]:
        return "User Was Not Blacklisted !"
    mn = Bl["USERS"]
    mn.remove(id)
    Bl.update({"USERS":mn})
    DB.set("BLACKLIST", str(Bl))
    return "Removed User from BLACKLIST"


def get_blacklisted():
    Bl = get_stuff("BLACKLIST")
    if not Bl:
        return []
    return Bl["USERS"]
