import discord
import requests
import json
import time
import threading
import asyncio
import webbrowser
import os
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor
import sys

os.system("title Ultimate Server Cloner - Developed by zle0o")
os.system("cls" if os.name == "nt" else "clear")

GREEN = "\033[92m"
RED = "\033[91m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

class RateLimiter:
    def __init__(self, calls_per_second=5):
        self.calls_per_second = calls_per_second
        self.last_call = 0
        self.lock = threading.Lock()
    
    def wait(self):
        with self.lock:
            current = time.time()
            time_since_last = current - self.last_call
            if time_since_last < (1.0 / self.calls_per_second):
                time.sleep((1.0 / self.calls_per_second) - time_since_last)
            self.last_call = time.time()

rate_limiter = RateLimiter(3)

def validate_token(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return f"{user_data['username']}"
        return None
    except Exception as e:
        return None

def get_guild_details(token, guild_id):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    try:
        response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}', headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def create_webhook_in_channel(token, channel_id, name):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    data = {"name": name}
    try:
        response = requests.post(f'https://discord.com/api/v10/channels/{channel_id}/webhooks', 
                               headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['url']
    except:
        pass
    return None

def fetch_all_messages(token, channel_id, limit=100):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    messages = []
    try:
        response = requests.get(f'https://discord.com/api/v10/channels/{channel_id}/messages?limit={limit}', 
                              headers=headers)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return messages

def animated_banner():
    banner = f"""{RED}
        ██████╗ ██████╗ ███████╗ █████╗ ███╗   ███╗    ██████╗██╗      ██████╗ ███╗   ██╗███████╗██████╗     ██╗   ██╗██████╗ 
        ██╔══██╗██╔══██╗██╔════╝██╔══██╗████╗ ████║    ██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝██╔══██╗    ██║   ██║╚════██╗
        ██║  ██║██████╔╝█████╗  ███████║██╔████╔██║    ██║     ██║     ██║   ██║██╔██╗ ██║█████╗  ██████╔╝    ██║   ██║ █████╔╝
        ██║  ██║██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║    ██║     ██║     ██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝██╔═══╝ 
        ██████╔╝██║  ██║███████╗██║  ██║██║ ╚═╝ ██║    ╚██████╗███████╗╚██████╔╝██║ ╚████║███████╗██║  ██║     ╚████╔╝ ███████╗
        ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝      ╚═══╝  ╚══════╝{RESET}"""
    return banner

def main_menu():
    while True:
        print("\033c" if os.name == "nt" else "\033[H\033[J", end='')
        print(animated_banner())
        print(f"""
                                    {CYAN}ULTIMATE SERVER CLONER{RESET}
                                  {PURPLE}Developed by zle0o{RESET}        

        {GREEN}[1]{RESET} > Clone Server (Full Replication)
        {GREEN}[2]{RESET} > Clone Server with Messages
        {GREEN}[3]{RESET} > Mass Clone (Multiple Targets)
        {GREEN}[4]{RESET} > Steal Emojis & Stickers
        {GREEN}[5]{RESET} > Export Server Settings
        {GREEN}[6]{RESET} > Join Support Server
        {GREEN}[7]{RESET} > Exit
        
        """)
        
        choice = input(f"{RED}[{RESET}{CYAN}SELECT{RESET}{RED}]{RESET} Choose option: ").strip()
        
        if choice == '1':
            token = input(f"\n[{GREEN}TOKEN{RESET}] Enter your Discord token: ").strip()
            
            print("\n" + "="*50)
            print(f"{CYAN}TOKEN VALIDATION IN PROGRESS...{RESET}")
            
            result = {'valid': False, 'username': None}
            def check_token():
                result['username'] = validate_token(token)
                result['valid'] = result['username'] is not None
            
            thread = threading.Thread(target=check_token)
            thread.start()
            
            animation = "|/-\\"
            for i in range(30):
                print(f"[{animation[i % len(animation)]}] Validating token... {i*3}%", end='\r')
                time.sleep(0.05)
            
            thread.join()
            print(f"\n[{GREEN}✓{RESET}] Validation complete!")
            
            if result['valid']:
                print(f"{GREEN}[SUCCESS]{RESET} Logged in as: {result['username']}")
                
                source_id = input(f"\n[{CYAN}SOURCE{RESET}] Enter source server ID: ").strip()
                target_id = input(f"[{CYAN}TARGET{RESET}] Enter target server ID: ").strip()
                
                message_limit = input(f"\n[{CYAN}LIMIT{RESET}] Message limit per channel (default 50): ").strip()
                message_limit = int(message_limit) if message_limit.isdigit() else 50
                
                print(f"\n{YELLOW}[SETUP MODE]{RESET}")
                print(f"{GREEN}[1]{RESET} > Fresh Setup (delete existing roles/channels)")
                print(f"{GREEN}[2]{RESET} > Keep Existing (merge with current server)")
                setup_mode = input(f"\n{RED}[{RESET}{CYAN}SELECT{RESET}{RED}]{RESET} Choose setup mode: ").strip()
                fresh_setup = setup_mode == '1'
                
                print(f"\n{YELLOW}[MESSAGE MODE]{RESET}")
                print(f"{GREEN}[1]{RESET} > Realistic (Webhooks - Original author info)")
                print(f"{GREEN}[2]{RESET} > Classic (Current user sends messages)")
                mode = input(f"\n{RED}[{RESET}{CYAN}SELECT{RESET}{RED}]{RESET} Choose message mode: ").strip()
                realistic_mode = mode == '1'
                
                print(f"\n{YELLOW}[INFO]{RESET} Starting full clone process...")
                print(f"{YELLOW}[INFO]{RESET} Source: {source_id}")
                print(f"{YELLOW}[INFO]{RESET} Target: {target_id}")
                print(f"{YELLOW}[INFO]{RESET} Setup Mode: {'Fresh' if fresh_setup else 'Keep Existing'}")
                print(f"{YELLOW}[INFO]{RESET} Messages: {message_limit} per channel")
                print(f"{YELLOW}[INFO]{RESET} Message Mode: {'Realistic' if realistic_mode else 'Classic'}")
                print("-"*50)
                
                if fresh_setup:
                    print(f"{YELLOW}[INFO]{RESET} Cleaning up target server...")
                    asyncio.run(clean_target_server(token, target_id))
                
                asyncio.run(clone_server_full(token, source_id, target_id, clone_messages=True, message_limit=message_limit, realistic_mode=realistic_mode))
                
                print(f"\n{YELLOW}[INFO]{RESET} Cloning emojis and stickers...")
                asyncio.run(clone_emojis_stickers(token, source_id, target_id))
                
                print(f"\n{GREEN}[COMPLETE]{RESET} Full server clone completed successfully!")
                input(f"\n[{CYAN}CONTINUE{RESET}] Press Enter to return to menu...")
            else:
                print(f"{RED}[-] Invalid token{RESET}")
                time.sleep(2)
        
        elif choice == '2':
            token = input(f"\n[{GREEN}TOKEN{RESET}] Enter your Discord token: ").strip()
            
            source_id = input(f"\n[{CYAN}SOURCE{RESET}] Enter source server ID: ").strip()
            target_id = input(f"[{CYAN}TARGET{RESET}] Enter target server ID: ").strip()
            
            message_limit = input(f"[{CYAN}LIMIT{RESET}] Message limit per channel (default 50): ").strip()
            message_limit = int(message_limit) if message_limit.isdigit() else 50
            
            print(f"\n{YELLOW}[MESSAGE MODE]{RESET}")
            print(f"{GREEN}[1]{RESET} > Realistic (Webhooks - Original author info)")
            print(f"{GREEN}[2]{RESET} > Classic (Current user sends messages)")
            mode = input(f"\n{RED}[{RESET}{CYAN}SELECT{RESET}{RED}]{RESET} Choose mode: ").strip()
            realistic_mode = mode == '1'
            
            print(f"\n{YELLOW}[INFO]{RESET} Starting advanced clone with messages...")
            asyncio.run(clone_server_advanced(token, source_id, target_id, message_limit, realistic_mode))
            input(f"\n[{CYAN}CONTINUE{RESET}] Press Enter to return to menu...")
        
        elif choice == '3':
            token = input(f"\n[{GREEN}TOKEN{RESET}] Enter your Discord token: ").strip()
            source_id = input(f"\n[{CYAN}SOURCE{RESET}] Enter source server ID: ").strip()
            
            targets = input(f"[{CYAN}TARGETS{RESET}] Enter target server IDs (comma-separated): ").strip()
            target_list = [t.strip() for t in targets.split(',')]
            
            print(f"\n{YELLOW}[INFO]{RESET} Starting mass clone to {len(target_list)} servers...")
            asyncio.run(mass_clone(token, source_id, target_list))
            input(f"\n[{CYAN}CONTINUE{RESET}] Press Enter to return to menu...")
        
        elif choice == '4':
            token = input(f"\n[{GREEN}TOKEN{RESET}] Enter your Discord token: ").strip()
            source_id = input(f"\n[{CYAN}SOURCE{RESET}] Enter source server ID: ").strip()
            target_id = input(f"[{CYAN}TARGET{RESET}] Enter target server ID: ").strip()
            
            print(f"\n{YELLOW}[INFO]{RESET} Stealing emojis and stickers...")
            asyncio.run(clone_emojis_stickers(token, source_id, target_id))
            input(f"\n[{CYAN}CONTINUE{RESET}] Press Enter to return to menu...")
        
        elif choice == '5':
            token = input(f"\n[{GREEN}TOKEN{RESET}] Enter your Discord token: ").strip()
            server_id = input(f"\n[{CYAN}SERVER{RESET}] Enter server ID to export: ").strip()
            
            print(f"\n{YELLOW}[INFO]{RESET} Exporting server settings...")
            export_server_config(token, server_id)
            input(f"\n[{CYAN}CONTINUE{RESET}] Press Enter to return to menu...")
        
        elif choice == '6':
            webbrowser.open("https://discord.gg/zhM6BwFrEv")
            print(f"\n{GREEN}[INFO]{RESET} Opening support server...")
            time.sleep(2)
        
        elif choice == '7':
            print(f"\n{RED}[EXIT]{RESET} Closing Ultimate Server Cloner...")
            for i in range(3, 0, -1):
                print(f"Exiting in {i}...", end='\r')
                time.sleep(1)
            sys.exit(0)
        
        else:
            print(f"{RED}[ERROR]{RESET} Invalid option!")
            time.sleep(1)

async def clean_target_server(token, target_id):
    """Delete all roles and channels from target server (except @everyone)"""
    headers = {"Authorization": token, "Content-Type": "application/json"}
    
    try:
        channels_response = requests.get(f'https://discord.com/api/v10/guilds/{target_id}/channels', 
                                        headers=headers)
        if channels_response.status_code == 200:
            channels = channels_response.json()
            for channel in channels:
                try:
                    requests.delete(f'https://discord.com/api/v10/channels/{channel["id"]}', 
                                  headers=headers)
                    print(f"{RED}[✓] Deleted channel: {channel.get('name', 'Unknown')}{RESET}")
                    time.sleep(0.3)
                except:
                    pass
        
        roles_response = requests.get(f'https://discord.com/api/v10/guilds/{target_id}/roles', 
                                     headers=headers)
        if roles_response.status_code == 200:
            roles = roles_response.json()
            for role in roles:
                if role['name'] != '@everyone':
                    try:
                        requests.delete(f'https://discord.com/api/v10/guilds/{target_id}/roles/{role["id"]}', 
                                      headers=headers)
                        print(f"{RED}[✓] Deleted role: {role['name']}{RESET}")
                        time.sleep(0.3)
                    except:
                        pass
        
        print(f"{YELLOW}[*] Target server cleaned!{RESET}")
    
    except Exception as e:
        print(f"{RED}[-] Error cleaning server: {str(e)}{RESET}")

async def clone_server_full(token, source_id, target_id, clone_messages=False, message_limit=100, realistic_mode=False):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    
    try:
        source_response = requests.get(f'https://discord.com/api/v10/guilds/{source_id}', headers=headers)
        if source_response.status_code != 200:
            print(f"{RED}[-] Source server not found or access denied{RESET}")
            return
        source = source_response.json()
        
        target_response = requests.get(f'https://discord.com/api/v10/guilds/{target_id}', headers=headers)
        if target_response.status_code != 200:
            print(f"{RED}[-] Target server not found or access denied{RESET}")
            return
        target = target_response.json()
        
        print(f"{CYAN}[*] Starting clone process...{RESET}")
        print(f"{CYAN}[*] Source: {source['name']}{RESET}")
        print(f"{CYAN}[*] Target: {target['name']}{RESET}")
        
        await clone_server_settings_rest(token, source, target)
        
        await clone_roles_rest(token, source_id, target_id)
        
        await clone_categories_channels_rest(token, source_id, target_id, clone_messages, message_limit, realistic_mode)
        
        print(f"{GREEN}[✓] Clone completed successfully!{RESET}")
        
    except Exception as e:
        print(f"{RED}[-] Error: {str(e)}{RESET}")

async def clone_server_settings(token, source, target):
    try:
        headers = {"Authorization": token, "Content-Type": "application/json"}
        
        icon_url = str(source.icon.url) if source.icon else None
        banner_url = str(source.banner.url) if source.banner else None
        splash_url = str(source.splash.url) if source.splash else None
        
        icon_data = None
        banner_data = None
        splash_data = None
        
        if icon_url:
            try:
                response = requests.get(icon_url)
                if response.status_code == 200:
                    import base64
                    icon_data = "data:image/png;base64," + base64.b64encode(response.content).decode()
            except:
                pass
        
        update_data = {
            "name": source.name,
            "description": source.description if hasattr(source, 'description') else None,
            "icon": icon_data,
            "verification_level": source.verification_level.value,
            "default_message_notifications": source.default_notifications.value,
            "explicit_content_filter": source.explicit_content_filter.value,
            "afk_timeout": source.afk_timeout,
            "afk_channel_id": str(source.afk_channel.id) if source.afk_channel else None,
            "system_channel_id": str(source.system_channel.id) if source.system_channel else None,
            "rules_channel_id": str(source.rules_channel.id) if source.rules_channel else None,
            "public_updates_channel_id": str(source.public_updates_channel.id) if source.public_updates_channel else None,
        }
        
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        response = requests.patch(f'https://discord.com/api/v10/guilds/{target.id}', 
                                headers=headers, json=update_data)
        
        if response.status_code == 200:
            print(f"{GREEN}[✓] Server settings cloned{RESET}")
        else:
            print(f"{RED}[-] Failed to clone some settings: {response.text}{RESET}")
    
    except Exception as e:
        print(f"{RED}[-] Error cloning settings: {str(e)}{RESET}")

async def clone_server_settings_rest(token, source, target):
    try:
        headers = {"Authorization": token, "Content-Type": "application/json"}
        
        update_data = {
            "name": source.get('name'),
        }
        
        icon_hash = source.get('icon')
        if icon_hash:
            try:
                icon_url = f"https://cdn.discordapp.com/icons/{source['id']}/{icon_hash}.png"
                icon_response = requests.get(icon_url)
                
                if icon_response.status_code == 200:
                    import base64
                    icon_data_b64 = base64.b64encode(icon_response.content).decode()
                    update_data['icon'] = f"data:image/png;base64,{icon_data_b64}"
                    print(f"{GREEN}[✓] Downloaded server icon{RESET}")
            except Exception as e:
                print(f"{RED}[-] Failed to download icon: {str(e)}{RESET}")
        
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        response = requests.patch(f'https://discord.com/api/v10/guilds/{target["id"]}', 
                                headers=headers, json=update_data)
        
        if response.status_code == 200:
            print(f"{GREEN}[✓] Server settings cloned{RESET}")
        else:
            print(f"{RED}[-] Failed to clone some settings: {response.status_code}{RESET}")
    
    except Exception as e:
        print(f"{RED}[-] Error cloning settings: {str(e)}{RESET}")

async def clone_roles(token, source, target):
    try:
        headers = {"Authorization": token, "Content-Type": "application/json"}
        
        for role in target.roles:
            if role.name != "@everyone" and role.position < target.me.top_role.position:
                try:
                    requests.delete(f'https://discord.com/api/v10/guilds/{target.id}/roles/{role.id}', 
                                  headers=headers)
                    print(f"{RED}[-] Deleted role: {role.name}{RESET}")
                except:
                    pass
        
        role_mapping = {}
        for role in reversed(source.roles):
            if role.name != "@everyone":
                try:
                    role_data = {
                        "name": role.name,
                        "permissions": str(role.permissions.value),
                        "color": role.color.value,
                        "hoist": role.hoist,
                        "mentionable": role.mentionable,
                        "position": role.position
                    }
                    
                    response = requests.post(f'https://discord.com/api/v10/guilds/{target.id}/roles', 
                                           headers=headers, json=role_data)
                    
                    if response.status_code == 200:
                        new_role_data = response.json()
                        role_mapping[role.id] = new_role_data['id']
                        print(f"{GREEN}[✓] Created role: {role.name}{RESET}")
                    
                    rate_limiter.wait()
                    
                except Exception as e:
                    print(f"{RED}[-] Failed to create role {role.name}: {str(e)}{RESET}")
        
        return role_mapping
    
    except Exception as e:
        print(f"{RED}[-] Error cloning roles: {str(e)}{RESET}")
        return {}

async def clone_roles_rest(token, source_id, target_id):
    try:
        headers = {"Authorization": token, "Content-Type": "application/json"}
        
        source_roles = requests.get(f'https://discord.com/api/v10/guilds/{source_id}/roles', 
                                   headers=headers).json()
        
        target_roles = requests.get(f'https://discord.com/api/v10/guilds/{target_id}/roles', 
                                   headers=headers).json()
        
        existing_role_names = {role['name'] for role in target_roles}
        
        role_mapping = {}
        for role in reversed(source_roles):
            if role['name'] != "@everyone":
                if role['name'] in existing_role_names:
                    print(f"{YELLOW}[*] Role already exists: {role['name']}{RESET}")
                    for target_role in target_roles:
                        if target_role['name'] == role['name']:
                            role_mapping[role['id']] = target_role['id']
                            break
                    continue
                
                try:
                    role_data = {
                        "name": role['name'],
                        "permissions": str(role['permissions']),
                        "color": role.get('color', 0),
                        "hoist": role.get('hoist', False),
                        "mentionable": role.get('mentionable', False),
                    }
                    
                    response = requests.post(f'https://discord.com/api/v10/guilds/{target_id}/roles', 
                                           headers=headers, json=role_data)
                    
                    if response.status_code == 200:
                        new_role_data = response.json()
                        role_mapping[role['id']] = new_role_data['id']
                        print(f"{GREEN}[✓] Created role: {role['name']}{RESET}")
                    
                    rate_limiter.wait()
                    
                except Exception as e:
                    print(f"{RED}[-] Failed to create role {role.get('name', 'Unknown')}: {str(e)}{RESET}")
        
        return role_mapping
    
    except Exception as e:
        print(f"{RED}[-] Error cloning roles: {str(e)}{RESET}")
        return {}

async def clone_categories_channels(token, source, target, clone_messages=False):
    try:
        headers = {"Authorization": token, "Content-Type": "application/json"}
        
        for channel in target.channels:
            try:
                requests.delete(f'https://discord.com/api/v10/channels/{channel.id}', headers=headers)
                print(f"{RED}[-] Deleted channel: {channel.name}{RESET}")
                rate_limiter.wait()
            except:
                pass
        
        category_mapping = {}
        
        for category in source.categories:
            try:
                category_data = {
                    "name": category.name,
                    "type": 4,
                    "position": category.position
                }
                
                response = requests.post(f'https://discord.com/api/v10/guilds/{target.id}/channels', 
                                       headers=headers, json=category_data)
                
                if response.status_code == 200:
                    new_category_data = response.json()
                    category_mapping[category.id] = new_category_data['id']
                    print(f"{GREEN}[✓] Created category: {category.name}{RESET}")
                
                rate_limiter.wait()
                
            except Exception as e:
                print(f"{RED}[-] Failed to create category {category.name}: {str(e)}{RESET}")
        
        for channel in source.channels:
            try:
                if not isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.StageChannel, discord.ForumChannel)):
                    continue
                
                channel_data = {
                    "name": channel.name,
                    "type": channel.type.value,
                    "position": channel.position,
                    "parent_id": category_mapping.get(channel.category_id) if channel.category else None,
                }
                
                if isinstance(channel, discord.TextChannel):
                    channel_data.update({
                        "topic": channel.topic,
                        "nsfw": channel.nsfw,
                        "rate_limit_per_user": channel.slowmode_delay,
                    })
                elif isinstance(channel, discord.VoiceChannel):
                    channel_data.update({
                        "bitrate": channel.bitrate,
                        "user_limit": channel.user_limit,
                    })
                
                response = requests.post(f'https://discord.com/api/v10/guilds/{target.id}/channels', 
                                       headers=headers, json=channel_data)
                
                if response.status_code == 200:
                    new_channel_data = response.json()
                    print(f"{GREEN}[✓] Created channel: {channel.name}{RESET}")
                    
                    if clone_messages and isinstance(channel, discord.TextChannel):
                        await clone_channel_messages(token, channel.id, new_channel_data['id'])
                
                rate_limiter.wait()
                
            except Exception as e:
                print(f"{RED}[-] Failed to create channel {channel.name}: {str(e)}{RESET}")
    
    except Exception as e:
        print(f"{RED}[-] Error cloning channels: {str(e)}{RESET}")

async def clone_categories_channels_rest(token, source_id, target_id, clone_messages=False, message_limit=100, realistic_mode=False):
    try:
        headers = {"Authorization": token, "Content-Type": "application/json"}
        
        source_channels = requests.get(f'https://discord.com/api/v10/guilds/{source_id}/channels', 
                                      headers=headers).json()
        
        target_channels = requests.get(f'https://discord.com/api/v10/guilds/{target_id}/channels', 
                                      headers=headers).json()
        
        existing_channel_names = {channel['name'] for channel in target_channels}
        existing_category_ids = {channel['id']: channel['id'] for channel in target_channels if channel['type'] == 4}
        
        category_mapping = {}
        
        for channel in source_channels:
            if channel['type'] == 4:
                if channel['name'] in existing_channel_names:
                    print(f"{YELLOW}[*] Category already exists: {channel['name']}{RESET}")
                    for target_channel in target_channels:
                        if target_channel['name'] == channel['name'] and target_channel['type'] == 4:
                            category_mapping[channel['id']] = target_channel['id']
                            break
                    continue
                
                try:
                    category_data = {
                        "name": channel['name'],
                        "type": 4,
                        "position": channel.get('position', 0)
                    }
                    
                    response = requests.post(f'https://discord.com/api/v10/guilds/{target_id}/channels', 
                                           headers=headers, json=category_data)
                    
                    if response.status_code == 201:
                        new_category_data = response.json()
                        category_mapping[channel['id']] = new_category_data['id']
                        print(f"{GREEN}[✓] Created category: {channel['name']}{RESET}")
                    
                    rate_limiter.wait()
                    
                except Exception as e:
                    print(f"{RED}[-] Failed to create category {channel.get('name', 'Unknown')}: {str(e)}{RESET}")
        
        for channel in source_channels:
            if channel['type'] != 4:
                if channel['name'] in existing_channel_names:
                    print(f"{YELLOW}[*] Channel already exists: {channel['name']}{RESET}")
                    for target_channel in target_channels:
                        if target_channel['name'] == channel['name'] and target_channel['type'] == channel['type']:
                            if clone_messages and channel['type'] == 0:
                                await clone_channel_messages(token, channel['id'], target_channel['id'], message_limit, realistic_mode)
                            break
                    continue
                
                try:
                    parent_id = None
                    if channel.get('parent_id'):
                        parent_id = category_mapping.get(channel.get('parent_id'))
                    
                    channel_data = {
                        "name": channel['name'],
                        "type": channel['type'],
                        "position": channel.get('position', 0),
                    }
                    
                    if parent_id:
                        channel_data["parent_id"] = parent_id
                    
                    if channel['type'] == 0:
                        channel_data.update({
                            "topic": channel.get('topic'),
                            "nsfw": channel.get('nsfw', False),
                            "rate_limit_per_user": channel.get('rate_limit_per_user', 0),
                        })
                    elif channel['type'] == 2:
                        channel_data.update({
                            "bitrate": channel.get('bitrate', 64000),
                            "user_limit": channel.get('user_limit', 0),
                        })
                    
                    response = requests.post(f'https://discord.com/api/v10/guilds/{target_id}/channels', 
                                           headers=headers, json=channel_data)
                    
                    if response.status_code == 201:
                        new_channel_data = response.json()
                        print(f"{GREEN}[✓] Created channel: {channel['name']}{RESET}")
                        
                        if clone_messages and channel['type'] == 0:
                            await clone_channel_messages(token, channel['id'], new_channel_data['id'], message_limit, realistic_mode)
                    else:
                        print(f"{RED}[-] Failed to create channel {channel['name']}: {response.status_code} - {response.text}{RESET}")
                    
                    rate_limiter.wait()
                    
                except Exception as e:
                    print(f"{RED}[-] Failed to create channel {channel.get('name', 'Unknown')}: {str(e)}{RESET}")
    
    except Exception as e:
        print(f"{RED}[-] Error cloning channels: {str(e)}{RESET}")

async def clone_server_advanced(token, source_id, target_id, message_limit=50, realistic_mode=False):
    await clone_server_full(token, source_id, target_id, clone_messages=True, message_limit=message_limit, realistic_mode=realistic_mode)

async def mass_clone(token, source_id, target_ids):
    for i, target_id in enumerate(target_ids, 1):
        print(f"\n{YELLOW}[*] Cloning to server {i}/{len(target_ids)}: {target_id}...{RESET}")
        await clone_server_full(token, source_id, target_id, clone_messages=False, message_limit=100)
        time.sleep(2)
    print(f"\n{GREEN}[✓] Mass clone completed! {len(target_ids)} servers cloned.{RESET}")

async def clone_emojis_stickers(token, source_id, target_id):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    
    try:
        source_emojis_response = requests.get(f'https://discord.com/api/v10/guilds/{source_id}/emojis', 
                                             headers=headers)
        
        if source_emojis_response.status_code != 200:
            print(f"{RED}[-] Failed to fetch source emojis: {source_emojis_response.status_code}{RESET}")
            source_emojis = []
        else:
            source_emojis = source_emojis_response.json()
        
        if len(source_emojis) == 0:
            print(f"{YELLOW}[*] No emojis to clone{RESET}")
        else:
            print(f"{YELLOW}[*] Found {len(source_emojis)} emojis to clone{RESET}")
        
        for emoji in source_emojis:
            try:
                emoji_url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.{'gif' if emoji['animated'] else 'png'}"
                emoji_response = requests.get(emoji_url)
                
                if emoji_response.status_code != 200:
                    print(f"{RED}[-] Failed to download emoji {emoji['name']}{RESET}")
                    continue
                
                import base64
                emoji_data_b64 = base64.b64encode(emoji_response.content).decode()
                emoji_type = 'image/gif' if emoji['animated'] else 'image/png'
                
                emoji_data = {
                    "name": emoji['name'],
                    "image": f"data:{emoji_type};base64,{emoji_data_b64}"
                }
                
                response = requests.post(f'https://discord.com/api/v10/guilds/{target_id}/emojis', 
                                       headers=headers, json=emoji_data)
                
                if response.status_code == 201:
                    print(f"{GREEN}[✓] Cloned emoji: {emoji['name']}{RESET}")
                else:
                    print(f"{RED}[-] Failed to create emoji {emoji['name']}: {response.status_code}{RESET}")
                
                rate_limiter.wait()
                
            except Exception as e:
                print(f"{RED}[-] Failed to clone emoji {emoji.get('name', 'Unknown')}: {str(e)}{RESET}")
        
        source_stickers_response = requests.get(f'https://discord.com/api/v10/guilds/{source_id}/stickers', 
                                               headers=headers)
        
        if source_stickers_response.status_code != 200:
            print(f"{RED}[-] Failed to fetch source stickers: {source_stickers_response.status_code}{RESET}")
            source_stickers = []
        else:
            source_stickers = source_stickers_response.json()
        
        if len(source_stickers) == 0:
            print(f"{YELLOW}[*] No stickers to clone{RESET}")
        else:
            print(f"{YELLOW}[*] Found {len(source_stickers)} stickers to clone{RESET}")
        
        for sticker in source_stickers:
            try:
                sticker_url = sticker.get('asset', '')
                if not sticker_url:
                    print(f"{RED}[-] No asset URL for sticker {sticker.get('name', 'Unknown')}{RESET}")
                    continue
                
                if not sticker_url.startswith('http'):
                    sticker_url = f"https://cdn.discordapp.com/stickers/{sticker['id']}.png"
                
                sticker_response = requests.get(sticker_url)
                
                if sticker_response.status_code != 200:
                    print(f"{RED}[-] Failed to download sticker {sticker['name']}{RESET}")
                    continue
                
                import base64
                sticker_data_b64 = base64.b64encode(sticker_response.content).decode()
                
                sticker_data = {
                    "name": sticker['name'],
                    "description": sticker.get('description', ''),
                    "tags": sticker.get('tags', ''),
                    "file": f"data:image/png;base64,{sticker_data_b64}"
                }
                
                files = {'file': sticker_response.content}
                data = {
                    'name': sticker['name'],
                    'description': sticker.get('description', ''),
                    'tags': sticker.get('tags', '')
                }
                
                response = requests.post(f'https://discord.com/api/v10/guilds/{target_id}/stickers', 
                                       headers={"Authorization": token},
                                       files=files,
                                       data=data)
                
                if response.status_code == 201:
                    print(f"{GREEN}[✓] Cloned sticker: {sticker['name']}{RESET}")
                else:
                    print(f"{RED}[-] Failed to create sticker {sticker['name']}: {response.status_code}{RESET}")
                
                rate_limiter.wait()
                
            except Exception as e:
                print(f"{RED}[-] Failed to clone sticker {sticker.get('name', 'Unknown')}: {str(e)}{RESET}")
        
        print(f"{GREEN}[✓] Emoji and sticker cloning complete!{RESET}")
    
    except Exception as e:
        print(f"{RED}[-] Error cloning emojis/stickers: {str(e)}{RESET}")

async def clone_channel_messages(token, source_channel_id, target_channel_id, limit=100, realistic_mode=False):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    
    MESSAGE_COOLDOWN = 5
    
    try:
        print(f"{YELLOW}[*] Cloning messages from channel {source_channel_id} (limit: {limit})...{RESET}")
        print(f"{YELLOW}[*] Mode: {'Realistic (Webhooks)' if realistic_mode else 'Classic (Direct)'}...{RESET}")
        
        messages_response = requests.get(f'https://discord.com/api/v10/channels/{source_channel_id}/messages?limit={limit}', 
                                        headers=headers)
        
        if messages_response.status_code == 403:
            print(f"{YELLOW}[*] No permission to read messages in this channel (restricted){RESET}")
            return
        elif messages_response.status_code != 200:
            print(f"{RED}[-] Failed to fetch messages: {messages_response.status_code}{RESET}")
            return
        
        messages = messages_response.json()
        
        if len(messages) == 0:
            print(f"{YELLOW}[*] No messages to clone{RESET}")
            return
        
        print(f"{YELLOW}[*] Found {len(messages)} messages to clone{RESET}")
        
        cloned_count = 0
        webhook_cache = {}
        
        for message in reversed(messages):
            try:
                if 'content' in message and message['content']:
                    
                    if realistic_mode and 'author' in message:
                        author = message['author']
                        author_name = author.get('username', 'Unknown')
                        author_id = author.get('id')
                        
                        if author_name not in webhook_cache:
                            avatar_url = None
                            if author.get('avatar'):
                                avatar_url = f"https://cdn.discordapp.com/avatars/{author_id}/{author['avatar']}.png"
                            
                            webhook_data = {"name": author_name}
                            
                            rate_limiter.wait()
                            
                            webhook_response = requests.post(
                                f'https://discord.com/api/v10/channels/{target_channel_id}/webhooks',
                                headers=headers,
                                json=webhook_data
                            )
                            
                            if webhook_response.status_code in [200, 201]:
                                webhook_info = webhook_response.json()
                                webhook_url = f"https://discord.com/api/webhooks/{webhook_info['id']}/{webhook_info['token']}"
                                webhook_cache[author_name] = {
                                    'url': webhook_url,
                                    'avatar': avatar_url,
                                    'id': webhook_info['id']
                                }
                                print(f"{GREEN}[✓] Created webhook for: {author_name}{RESET}")
                            elif webhook_response.status_code == 429:
                                print(f"{YELLOW}[*] Rate limited, waiting...{RESET}")
                                time.sleep(2)
                                webhook_response = requests.post(
                                    f'https://discord.com/api/v10/channels/{target_channel_id}/webhooks',
                                    headers=headers,
                                    json=webhook_data
                                )
                                if webhook_response.status_code in [200, 201]:
                                    webhook_info = webhook_response.json()
                                    webhook_url = f"https://discord.com/api/webhooks/{webhook_info['id']}/{webhook_info['token']}"
                                    webhook_cache[author_name] = {
                                        'url': webhook_url,
                                        'avatar': avatar_url,
                                        'id': webhook_info['id']
                                    }
                                    print(f"{GREEN}[✓] Created webhook for: {author_name}{RESET}")
                                else:
                                    webhook_cache[author_name] = None
                            else:
                                webhook_cache[author_name] = None
                        
                        webhook_info = webhook_cache.get(author_name)
                        if webhook_info:
                            webhook_payload = {
                                "content": message['content'],
                                "username": author_name,
                            }
                            
                            if webhook_info.get('avatar'):
                                webhook_payload['avatar_url'] = webhook_info['avatar']
                            
                            if message.get('embeds'):
                                webhook_payload['embeds'] = message['embeds']
                            
                            webhook_send = requests.post(
                                webhook_info['url'],
                                json=webhook_payload
                            )
                            
                            if webhook_send.status_code in [200, 204]:
                                cloned_count += 1
                            elif webhook_send.status_code == 429:
                                print(f"{YELLOW}[*] Rate limited, waiting 3 seconds...{RESET}")
                                time.sleep(3)
                                webhook_send = requests.post(
                                    webhook_info['url'],
                                    json=webhook_payload
                                )
                                if webhook_send.status_code in [200, 204]:
                                    cloned_count += 1
                            
                            time.sleep(MESSAGE_COOLDOWN)
                    
                    else:
                        message_data = {
                            "content": message['content'],
                            "tts": False,
                            "embeds": message.get('embeds', []),
                            "components": message.get('components', [])
                        }
                        
                        response = requests.post(f'https://discord.com/api/v10/channels/{target_channel_id}/messages', 
                                               headers=headers, json=message_data)
                        
                        if response.status_code == 201:
                            cloned_count += 1
                        elif response.status_code == 429:
                            print(f"{YELLOW}[*] Rate limited, waiting...{RESET}")
                            time.sleep(2)
                            response = requests.post(f'https://discord.com/api/v10/channels/{target_channel_id}/messages', 
                                                   headers=headers, json=message_data)
                            if response.status_code == 201:
                                cloned_count += 1
                        
                        time.sleep(MESSAGE_COOLDOWN)
                        
            except Exception as e:
                continue
        
        if cloned_count > 0:
            print(f"{GREEN}[✓] Cloned {cloned_count} messages{RESET}")
    
    except Exception as e:
        print(f"{RED}[-] Error cloning messages: {str(e)}{RESET}")

def export_server_config(token, server_id):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    
    try:
        server_response = requests.get(f'https://discord.com/api/v10/guilds/{server_id}', 
                                      headers=headers)
        
        if server_response.status_code != 200:
            print(f"{RED}[-] Server not found or access denied: {server_response.status_code}{RESET}")
            return
        
        server_data = server_response.json()
        
        roles_response = requests.get(f'https://discord.com/api/v10/guilds/{server_id}/roles', 
                                     headers=headers)
        roles = roles_response.json() if roles_response.status_code == 200 else []
        
        channels_response = requests.get(f'https://discord.com/api/v10/guilds/{server_id}/channels', 
                                        headers=headers)
        channels = channels_response.json() if channels_response.status_code == 200 else []
        
        export_data = {
            "server_info": server_data,
            "roles": roles,
            "channels": channels,
            "export_timestamp": time.time(),
            "export_tool": "Ultimate Server Cloner v2"
        }
        
        filename = f"server_export_{server_id}_{int(time.time())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"{GREEN}[✓] Server configuration exported to {filename}{RESET}")
        print(f"{CYAN}[*] Contains: {len(roles)} roles, {len(channels)} channels{RESET}")
    
    except Exception as e:
        print(f"{RED}[-] Error exporting server config: {str(e)}{RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Interrupted by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}[FATAL ERROR] {str(e)}{RESET}")
        input("Press Enter to exit...")
        sys.exit(1)
