import hikari
import miru


def get_role_view(guild_id):
    if guild_id == 994181854058000416:
        view = RoleView1A()
    elif guild_id == 890968871845122108:
        view = RoleView2A()
    else:
        raise ValueError
    return view


class RoleView1A(miru.View):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(timeout=None, *args, **kwargs)

    roles_id = {
        'A': 994193658242932776,
        'A1': 994193894038327306,
        'A2': 994193958924202025,
        'B': 994193814585614386,
        'B1': 994194055443517470,
        'B2': 994194085009182730,
        'C': 994193848236515378,
        'C1': 994194108748931183,
        'C2': 994194139954544661,
        'D': 994193883300900874,
        'D1': 994196538022711307,
        'D2': 994196567252795503,
        'E': 1014167315719401524,
        'E1': 1014167472867397722,
        'E2': 1014167522364366949,
        'S0': 1077700243530977372,
    }

    roles_group = {
        "TP A1": [roles_id.get("A"), roles_id.get("A1")],
        "TP A2": [roles_id.get("A"), roles_id.get("A2")],
        "TP B1": [roles_id.get("B"), roles_id.get("B1")],
        "TP B2": [roles_id.get("B"), roles_id.get("B2")],
        "TP C1": [roles_id.get("C"), roles_id.get("C1")],
        "TP C2": [roles_id.get("C"), roles_id.get("C2")],
        "TP D1": [roles_id.get("D"), roles_id.get("D1")],
        "TP D2": [roles_id.get("D"), roles_id.get("D2")],
        "TP E1": [roles_id.get("E"), roles_id.get("E1")],
        "TP E2": [roles_id.get("E"), roles_id.get("E2")],
        "SO": [roles_id.get("S0")],
    }

    @miru.text_select(
        custom_id="Selecteur_Groupe",
        placeholder="Groupes",
        options=[miru.SelectOption(label=nom_groupe_TP) for nom_groupe_TP in roles_group.keys()] + [miru.SelectOption(label="Aucun")],
    )
    async def role_select(self, select: miru.TextSelect, ctx: miru.Context) -> None:
        # liste des rôles que l'utilisateur a déjà parmis les ID des roles (A, A1, A2, B, etc)
        liste_roles = [id_role for nom_role, id_role in self.roles_id.items() if id_role in [role.id for role in ctx.member.get_roles()]]
        # suppression des anciens roles de l'utilisateur (ancien groupe TP et TD)
        for id_role in liste_roles:
            await ctx.member.remove_role(id_role)

        if select.values[0] == "Aucun":
            await ctx.respond("Vos rôles de groupe ont été supprimés.", flags=hikari.MessageFlag.EPHEMERAL)
            return

        # ajout des nouveaux roles de l'utilisateur, sélectionnés dans le menu (on ajoute un groupe TP et un groupe TD)
        for id_role in self.roles_group.get(select.values[0]):
            await ctx.member.add_role(id_role)

        added_roles = ", ".join(f"<@&{role}>" for role in self.roles_group.get(select.values[0]))
        await ctx.respond(f"Vous avez désormais {added_roles} !", flags=hikari.MessageFlag.EPHEMERAL)


class RoleView2A(miru.View):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(timeout=None, *args, **kwargs)

    roles_id = {
        "A1": 1005468359191691274,
        "A11": 1005431453800218664,
        "A12": 1005431520384794636,
        "A2": 1005468366175219882,
        "A21": 1005431589787934744,
        "A22": 1005431617038327808,
        "A3": 1005468505451266138,
        "A31": 1005431639050047508,
        "A32": 1005431663569940570,
        "B1": 1005468289314594816,
        "B11": 1005431187961036800,
        "B12": 1005431249885732924
    }

    roles_group = {
        "TP A11": [roles_id.get("A1"), roles_id.get("A11")],
        "TP A12": [roles_id.get("A1"), roles_id.get("A12")],
        "TP A21": [roles_id.get("A2"), roles_id.get("A21")],
        "TP A22": [roles_id.get("A2"), roles_id.get("A22")],
        "TP A31": [roles_id.get("A3"), roles_id.get("A31")],
        "TP A32": [roles_id.get("A3"), roles_id.get("A32")],
        "TP B11": [roles_id.get("B1"), roles_id.get("B11")],
        "TP B12": [roles_id.get("B1"), roles_id.get("B12")],
    }

    @miru.text_select(
        custom_id="Selecteur_Groupe",
        placeholder="Groupes",
        options=[miru.SelectOption(label=nom_groupe_TP) for nom_groupe_TP in roles_group.keys()] + [miru.SelectOption(label="Aucun")],
    )
    async def role_select(self, select: miru.TextSelect, ctx: miru.Context) -> None:
        # liste des rôles que l'utilisateur a déjà parmis les ID des roles (A, A1, A2, B, etc)
        liste_roles = [id_role for nom_role, id_role in self.roles_id.items() if id_role in [role.id for role in ctx.member.get_roles()]]
        # suppression des anciens roles de l'utilisateur (ancien groupe TP et TD)
        for id_role in liste_roles:
            await ctx.member.remove_role(id_role)

        if select.values[0] == "Aucun":
            await ctx.respond("Vos rôles de groupe ont été supprimés.", flags=hikari.MessageFlag.EPHEMERAL)
            return

        # ajout des nouveaux roles de l'utilisateur, sélectionnés dans le menu (on ajoute un groupe TP et un groupe TD)
        for id_role in self.roles_group.get(select.values[0]):
            await ctx.member.add_role(id_role)

        await ctx.respond(f"Vous avez désormais les rôles <@&{self.roles_group.get(select.values[0])[0]}> et <@&{self.roles_group.get(select.values[0])[1]}> !", flags=hikari.MessageFlag.EPHEMERAL)

