import discord, asyncio
from discord import app_commands
from discord.ext import tasks
from discord.ui import Button, View
from discord import ButtonStyle
import time
import random

class aclient(discord.Client):
    def init(self):
        super().init(intents = discord.Intents.all())
        self.synced = False
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True

client = aclient(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

token = 'MTM5NDQ4MDczMDQxMDg0ODQzOA.GzCM9q.ExlfJ9-Nkj5R5HLdn6RAQHk14PUJAaAmYxUmKM'

role_id = 1395359974603096154
admin = 1360568070686511202
log_channel = 1395361422162133103
ban_channel = 1303535093163495515

macro_random_min = 1800
macro_random_max = 2700

macro_dead_time = 120

voice_time_min = 1800

userList = []
userMacro = []
userRank = []

@client.event
async def on_ready():
    print("봇 기동 시작")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("활동률 이벤트 많관부!"))
    antimacro.start()
    MacroTimeCheck.start()
    await tree.sync()

@client.event
async def on_voice_state_update(member, before, after):

    username = member.display_name
    userid = member.mention

    for i in range(0, len(userList), 1):
        if (userList[i]["name"] == username):
            userMacro[i]["banned"] = False
            

    role = member.roles

    isExistRole = False
    for i in range(0, len(role), 1):
        if (role[i].id == role_id):
            isExistRole = True
            break

    if (not isExistRole):
        return

    
    ch=client.get_channel(log_channel)
    if not before.channel and after.channel:
        print(username, 'joined', after.channel)
        embed = discord.Embed(description=f"{userid} 님이 {after.channel.mention}에 입장하셨습니다!", color=0x00ff00)
        embed.set_author(name=username, icon_url=member.display_avatar)

        await ch.send(embed=embed)

        #await ch.send(f"{userid} 님이 {after.channel}에 입장하셨습니다.")
        isexistNameinList = False
        index = 0
        for i in range(0, len(userList), 1):
            isexistNameinList = True
            if (userList[i]['name'] == username):
                index = i
                break
            isexistNameinList = False

        if (not isexistNameinList):
            userList.append({"member": member, "name": username, "joinTime": 0, "leftTime": 0, "timeCount": 0})
            userMacro.append({"MacroBaseTime": 0, "AntiMacroTime": 0, "MacroRanNum": random.randint(macro_random_min, macro_random_max), "Banned": False, "isJoinRoom": False, "isVerify": False, "CheckButton": False})
            userList[len(userList) - 1]['joinTime'] = time.time()
            userMacro[len(userList) - 1]['MacroBaseTime'] = time.time()
            userMacro[len(userList) - 1]['isJoinRoom'] = True
        else:
            userList[index]['joinTime'] = time.time()
            userMacro[index]['MacroBaseTime'] = time.time()
            userMacro[index]['isJoinRoom'] = True

        embed = discord.Embed(title="현재 인원제한방에 들어와 있습니다!", description="인원 제한방에 머무른 시간은 기록으로 인정되지 않으니 주의하시기 바랍니다.", color=0xff00ff)

        if (after.channel.category_id == ban_channel):
            if (userList[i]['member'].dm_channel):
                await userList[i]['member'].dm_channel.send(embed=embed)

            elif (userList[i]['member'].dm_channel is None):
                channel = await userList[i]['member'].create_dm()
                await channel.send(embed=embed)

        

    if not after.channel and before.channel:
        print(username, 'leaved', before.channel)
        #await ch.send(f"{userid}님이 {before.channel}에서 퇴장하셨습니다.")

        index = 0
        for i in range(0, len(userList), 1):
            if (userList[i]['name'] == username):
                index = i
                userMacro[i]['isJoinRoom'] = False
                userList[i]['leftTime'] = time.time()
                if (not userMacro[i]['Banned'] and userList[i]['leftTime'] - userList[i]['joinTime'] >= voice_time_min and before.channel.category_id != ban_channel):
                    userList[i]['timeCount'] += userList[i]['leftTime'] - userList[i]['joinTime']
                elif (userMacro[i]['Banned']):
                    embed = discord.Embed(title="시간이 누적되지 않음", description=f"{userid}님은 잠수 방지 메시지에 응답하지 않았기에 시간이 누적되지 않았습니다.", color=0xff00ff)
                    embed.set_author(name=username, icon_url=member.display_avatar)
                    await ch.send(embed=embed)
                elif (userList[i]['leftTime'] - userList[i]['joinTime'] < voice_time_min):
                    embed = discord.Embed(title="시간이 누적되지 않음", description=f"{userid}님은 통화방에서 30분 이상 머무르지 않았기에 시간이 누적되지 않았습니다.", color=0xff00ff)
                    embed.set_author(name=username, icon_url=member.display_avatar)
                    await ch.send(embed=embed)
                elif (before.channel.category_id == ban_channel):
                    embed = discord.Embed(title="시간이 누적되지 않음", description=f"{userid}님은 인원제한방에 머물렀기에 시간이 누적되지 않았습니다.", color=0xff00ff)
                    embed.set_author(name=username, icon_url=member.display_avatar)
                    await ch.send(embed=embed)
                print(f'입장시간: {userList[i]['joinTime']}\n퇴장시간: {userList[i]['leftTime']}\n시간 누적치: {userList[i]['timeCount']}')

                embed = discord.Embed(description=f"{userid} 님이 {before.channel.mention}에서 퇴장하셨습니다!", color=0xff0000)
                embed.set_author(name=username, icon_url=member.display_avatar)
                embed.add_field(name="체류 시간", value=f"{round(userList[i]['leftTime'] - userList[i]['joinTime'], 2)}", inline=False)
                embed.add_field(name="시간 누적치", value=f"{round(userList[i]['timeCount'], 2)}", inline=False)

                await ch.send(embed=embed)
                #await ch.send(f'입장시간: {round(userList[i]['joinTime'], 2)}\n퇴장시간: {round(userList[i]['leftTime'], 2)}\n음성채널 체류 기간: {}\n시간 누적치: {round(userList[i]['timeCount'], 2)}')
                break

    if after.channel and before.channel:
        

        print(username, 'leaved', before.channel)
        #await ch.send(f"{userid}님이 {before.channel}에서 퇴장하셨습니다.")

        index = 0
        for i in range(0, len(userList), 1):
            if (userList[i]['name'] == username):
                index = i
                userMacro[i]['isJoinRoom'] = False
                userList[i]['leftTime'] = time.time()
                if (not userMacro[i]['Banned'] and userList[i]['leftTime'] - userList[i]['joinTime'] >= voice_time_min and before.channel.category_id != ban_channel):
                    userList[i]['timeCount'] += userList[i]['leftTime'] - userList[i]['joinTime']
                elif (userMacro[i]['Banned']):
                    embed = discord.Embed(title="시간이 누적되지 않음", description=f"{userid}님은 잠수 방지 메시지에 응답하지 않았기에 시간이 누적되지 않았습니다.", color=0xff00ff)
                    embed.set_author(name=username, icon_url=member.display_avatar)
                    await ch.send(embed=embed)
                elif (userList[i]['leftTime'] - userList[i]['joinTime'] < voice_time_min):
                    embed = discord.Embed(title="시간이 누적되지 않음", description=f"{userid}님은 통화방에서 30분 이상 머무르지 않았기에 시간이 누적되지 않았습니다.", color=0xff00ff)
                    embed.set_author(name=username, icon_url=member.display_avatar)
                    await ch.send(embed=embed)
                elif (before.channel.category_id == ban_channel):
                    embed = discord.Embed(title="시간이 누적되지 않음", description=f"{userid}님은 인원제한방에 머물렀기에 시간이 누적되지 않았습니다.", color=0xff00ff)
                    embed.set_author(name=username, icon_url=member.display_avatar)
                    await ch.send(embed=embed)
                print(f'입장시간: {userList[i]['joinTime']}\n퇴장시간: {userList[i]['leftTime']}\n시간 누적치: {userList[i]['timeCount']}')

                embed = discord.Embed(description=f"{userid} 님이 {before.channel.mention}에서 퇴장하셨습니다!", color=0xff0000)
                embed.set_author(name=username, icon_url=member.display_avatar)
                embed.add_field(name="체류 시간", value=f"{round(userList[i]['leftTime'] - userList[i]['joinTime'], 2)}", inline=False)
                embed.add_field(name="시간 누적치", value=f"{round(userList[i]['timeCount'], 2)}", inline=False)

                await ch.send(embed=embed)
                #await ch.send(f'입장시간: {round(userList[i]['joinTime'], 2)}\n퇴장시간: {round(userList[i]['leftTime'], 2)}\n음성채널 체류 기간: {}\n시간 누적치: {round(userList[i]['timeCount'], 2)}')
                break

        embed = discord.Embed(title="현재 인원제한방에 들어와 있습니다!", description="인원 제한방에 머무른 시간은 기록으로 인정되지 않으니 주의하시기 바랍니다.", color=0xff00ff)

        if (after.channel.category_id == ban_channel):
            if (userList[i]['member'].dm_channel):
                await userList[i]['member'].dm_channel.send(embed=embed)

            elif (userList[i]['member'].dm_channel is None):
                channel = await userList[i]['member'].create_dm()
                await channel.send(embed=embed)

        print(username, 'joined', after.channel)
        embed = discord.Embed(description=f"{userid} 님이 {after.channel.mention}에 입장하셨습니다!", color=0x00ff00)
        embed.set_author(name=username, icon_url=member.display_avatar)

        await ch.send(embed=embed)

        #await ch.send(f"{userid} 님이 {after.channel}에 입장하셨습니다.")
        
        userList[index]['joinTime'] = time.time()
        userMacro[index]['MacroBaseTime'] = time.time()
        userMacro[index]['isJoinRoom'] = True

            

@tree.command(name='전체순위', description='현재 누적된 시간 순위를 봅니다.')
async def rank(interaction: discord.Interaction):
    urank = sorted(userList, key=lambda userList: (userList['timeCount']), reverse=True)
    rankstr = ""
    for i in range(0, len(userList), 1):
        h = round(urank[i]['timeCount'] / 360)
        m = round(urank[i]['timeCount'] / 60) % 60
        s = round(urank[i]['timeCount'] % 60, 2)

        rankstr += f'{i+1}위: {urank[i]['name']} (시간 누적치: {h}시간 {m}분 {s}초)\n'
        if (i == 9):
            break
    await interaction.response.send_message("```" + rankstr + "```", ephemeral=False)

@tree.command(name="내시간", description="현재까지 누적된 시간을 봅니다.")
async def mytime(interaction: discord.Interaction):
    isexist = False
    index = 0
    for i in range(0, len(userList), 1):
        if (userList[i]['name'] == interaction.user.display_name):
            isexist = True
            index = i
            break

    h = round(userList[index]['timeCount'] / 360)
    m = round(userList[index]['timeCount'] / 60) % 60
    s = round(userList[index]['timeCount'] % 60, 2)

    if (isexist):
        embed = discord.Embed(title=f"{interaction.user.display_name}님의 시간 누적치", description=f"{h}시간 {m}분 {s}초", color=0x00ffff)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title=f"{interaction.user.display_name}님은 통화방에 참여한 기록이 없습니다.", color=0x00ffff)
        await interaction.response.send_message(embed=embed, ephemeral=True)



@tree.command(name="시간변경", description="이벤트 참여자의 누적 시간을 변경합니다. (관리자 전용)")
async def timeChange(interaction: discord.Interaction, member: discord.User, count: float):
    tempcount = 0

    role = interaction.user.roles

    isExistRole = False
    for i in range(0, len(role), 1):
        if (role[i].id == admin):
            isExistRole = True
            break

    if (not isExistRole):
        return
    
    index = 0
    for i in range(0, len(userList), 1):
        if (userList[i]['name'] == member.display_name):
            index = i
            tempcount = userList[i]['timeCount']
            userList[i]['timeCount'] = count
            break

    embed = discord.Embed(title="수정을 완료했습니다!", description=f"{interaction.user.mention}의 시간 누적치: {tempcount} -> {userList[index]['timeCount']}", color=0xffff00)
    await interaction.response.send_message(embed=embed)

@tree.command(name="시간보기", description="이벤트 참여자의 누적 시간을 봅니다. (관리자 전용)")
async def timeseek(interaction: discord.Interaction, member: discord.User):
    role = interaction.user.roles

    isExistRole = False
    for i in range(0, len(role), 1):
        if (role[i].id == admin):
            isExistRole = True
            break

    if (not isExistRole):
        return
    
    index = 0
    for i in range(0, len(userList), 1):
        if (userList[i]['name'] == member.display_name):
            index = i
            break
    
    embed = discord.Embed(description=f"{interaction.user.mention}의 시간 누적치: {userList[index]['timeCount']}", color=0xffff00)
    embed.set_author(name=member.display_name, icon_url=member.display_avatar)
    await interaction.response.send_message(embed=embed)

            

@tasks.loop(seconds=1)
async def antimacro():
    for i in range(0, len(userMacro), 1):
        if (time.time() - userMacro[i]['MacroBaseTime'] >= userMacro[i]['MacroRanNum'] and userMacro[i]['isJoinRoom']):
            print("감지 완료!")

            embed = discord.Embed(title=":no_entry: 잠수 방지 메시지입니다. :no_entry:", color=0xff0000)
            embed.add_field(name="2분 내로 버튼을 눌러주세요!", value="잠수 방지 버튼을 누르지 않을 시 시간이 누적되지 않습니다.", inline=False)

            button = Button(label="저는 잠수가 아닙니다!", style=ButtonStyle.green)
            view = View()
            view.add_item(button)

            userMacro[i]['MacroBaseTime'] = time.time()
            userMacro[i]['MacroRanNum'] = random.randint(macro_random_min, macro_random_max)
            userMacro[i]['AntiMacroTime'] = time.time()
            userMacro[i]['isVerify'] = True

            if (userList[i]['member'].dm_channel):
                await userList[i]['member'].dm_channel.send(embed=embed, view=view)

            elif (userList[i]['member'].dm_channel is None):
                channel = await userList[i]['member'].create_dm()
                await channel.send(embed=embed, view=view)

            async def button_callback(interaction: discord.Interaction):
                if (not userMacro[i]['isVerify']):
                    return
                embed = discord.Embed(title=":white_check_mark: 확인되었습니다", description="응답해주셔서 감사합니다!", color=0x00ff00)
                await interaction.response.send_message(embed=embed)
                userMacro[i]['CheckButton'] = True
            button.callback = button_callback

@tasks.loop(seconds=1)
async def MacroTimeCheck():
    for i in range(0, len(userMacro), 1):
        if (userMacro[i]['CheckButton']):
            userMacro[i]['isVerify'] = False
            userMacro[i]['CheckButton'] = False
            continue

        if (time.time() - userMacro[i]['AntiMacroTime'] >= macro_dead_time and userMacro[i]['isVerify'] and userMacro[i]['isJoinRoom']):
            print("잠수 감지")
            embed = discord.Embed(title=":rotating_light: 잠수가 감지되었습니다! :rotating_light:", description="현재 통화방에 기록된 시간이 무효 처리됩니다.", color=0xff0000)
            userMacro[i]['isVerify'] = False

            userMacro[i]['Banned'] = True
            await userList[i]['member'].dm_channel.send(embed=embed)
            return
            


client.run(token)
