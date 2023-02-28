import discord


class Roles:
    def __init__(self, guild: discord.Guild):
        self.dg_guild = guild
        self.staff_role = self.dg_guild.get_role(1054151799516446742) # @・STAFF 0
        self.support_role = self.dg_guild.get_role(1053765580701831168) # @・Support 1
        self.control_role = self.dg_guild.get_role(1053766515700273172) # @・Control 2
        self.moder_role = self.dg_guild.get_role(1053692457625333830) # @・Moderator 3
        self.curator_role = self.dg_guild.get_role(1019585554016391199) # @・Curator 4
        self.admin_role = self.dg_guild.get_role(957249264751378492) # @・Administrator 5
        self.transparent1_role = self.dg_guild.get_role(921729278188597259) # пустышка админка которая в самом низу 6
        self.heart_role = self.dg_guild.get_role(960642805099810816) # @🤍 7 
        self.cloud_role = self.dg_guild.get_role(960643635613933661) # @☁️ 8
        self.raincloud_role = self.dg_guild.get_role(960642444498731108) # @🌩 9
        self.transparent2_role = self.dg_guild.get_role(937676066066149407) # пустышка админка которая под скрепкой 10
        self.clip_role = self.dg_guild.get_role(980837561335414785) # @🧷 11
        self.deathgun_role = self.dg_guild.get_role(989882589600948234) # @Death Gun 12
        
    def get_all_staff_roles(self):
        staff_roles_list = [
            self.staff_role,
            self.support_role,
            self.control_role,
            self.moder_role, 
            self.curator_role,
            self.admin_role,
            self.transparent1_role,
            self.heart_role,
            self.cloud_role,
            self.raincloud_role,
            self.transparent2_role,
            self.clip_role,
            self.deathgun_role
        ]
        return staff_roles_list
    
    def roles_check(self, *, member: discord.Member, roles_list: list):
        return [x for x in member.roles if x in roles_list]
