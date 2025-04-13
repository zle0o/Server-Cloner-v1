import discord
import requests
import time
import threading
import asyncio
import webbrowser
import os

os.system("title Dream Cloner - Developed by zle0o")

GREEN = "\033[92m"
RED = "\033[91m"
PURPLE = "\033[95m"
RESET = "\033[0m"

def validate_token(token):
    headers = {"Authorization": token}
    try:
        response = requests.get('https://discord.com/api/v{10}', headers=headers)
        if response.status_code == 200:
            return response.json()['username']
        else:
            return None
    except:
        return None

def main_menu():
    while True:
        print("\033c", end='')
        print(f"""
          {RED}██████╗ ██████╗ ███████╗ █████╗ ███╗   ███╗     ██████╗██╗      ██████╗ ███╗   ██╗███████╗██████╗{RESET}
          {RED}██╔══██╗██╔══██╗██╔════╝██╔══██╗████╗ ████║    ██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝██╔══██╗{RESET}
          {RED}██║  ██║██████╔╝█████╗  ███████║██╔████╔██║    ██║     ██║     ██║   ██║██╔██╗ ██║█████╗  ██████╔╝{RESET}
          {RED}██║  ██║██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║    ██║     ██║     ██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗{RESET}
          {RED}██████╔╝██║  ██║███████╗██║  ██║██║ ╚═╝ ██║    ╚██████╗███████╗╚██████╔╝██║ ╚████║███████╗██║  ██║{RESET}
          {RED}╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝{RESET}
              
                                           {PURPLE}Developed by zle0o{RESET}

[1] > Clone Server
[2] > Join Discord Server
[3] > Exit
        """)
        choice = input(f"[{RED}>{RESET}] Choose: ")
        
        if choice == '1':
            token = input("\nEnter your Discord account token: ")
            print("\033c", end='')
            
            result = {'valid': False, 'username': None}
            def check_token():
                result['username'] = validate_token(token)
                result['valid'] = result['username'] is not None
            
            thread = threading.Thread(target=check_token)
            thread.start()
            
            print("Checking token...\n")
            for i in range(1, 21):
                print(f"[{'#' * i}{' ' * (20 - i)}] {i * 5}%", end='\r')
                time.sleep(0.1)
            thread.join()
            
            if result['valid']:
                print(f"\nLogged In as: {result['username']}")
                source_id = input("\nEnter source server ID: ")
                target_id = input("Enter target server ID: ")
                print("\nCloning Server")
                asyncio.run(clone_server(token, source_id, target_id))
                
                while True:
                    action = input("\nDo you want to go back to the menu or close the program? (back/close): ").strip().lower()
                    if action == "back":
                        break
                    elif action == "close":
                        print("Exiting...")
                        return
                    else:
                        print("Invalid choice. Please enter 'back' or 'close'.")
            else:
                print("\nInvalid token!")
            
        elif choice == '2':
            webbrowser.open("https://discord.gg/hbpH4e2CZQ")
            
        elif choice == '3':
            print("Exiting...")
            break

async def clone_server(token, source_id, target_id):
    
    intents = discord.Intents.default()
    intents.guilds = True  
    intents.members = True  
    
    
    client = discord.Client(intents=intents)
    
    try:
        await client.login(token)
        print(f"{GREEN}[+] Login successful!{RESET}")
    except discord.LoginFailure:
        print(f"{RED}[-] Login failed: Improper token has been passed.{RESET}")
        return
    except Exception as e:
        print(f"{RED}[-] An error occurred during login: {e}{RESET}")
        return

    @client.event
    async def on_ready():
        try:
            source = client.get_guild(int(source_id))
            target = client.get_guild(int(target_id))
            
            print(f"Source: {source}")
            print(f"Target: {target}")

            if not source:
                print(f"{RED}[-] Source server not found or inaccessible.{RESET}")
                await client.close()
                return
            if not target:
                print(f"{RED}[-] Target server not found or inaccessible.{RESET}")
                await client.close()
                return

            if not source.roles:
                print(f"{RED}[-] No roles found in the source server.{RESET}")
                await client.close()
                return
            if not source.categories:
                print(f"{RED}[-] No categories found in the source server.{RESET}")
                await client.close()
                return

            for role in target.roles:
                if role.name != "@everyone":
                    try:
                        await role.delete()
                        print(f"{RED}[-] Deleted Role: {role.name}{RESET}")
                    except Exception as e:
                        print(f"{RED}[-] Failed to delete role {role.name}: {e}{RESET}")
            
            for channel in target.channels:
                try:
                    await channel.delete()
                    print(f"{RED}[-] Deleted Channel: {channel.name}{RESET}")
                except Exception as e:
                    print(f"{RED}[-] Failed to delete channel {channel.name}: {e}{RESET}")
            
            try:
                icon_url = str(source.icon.url) if source.icon else None
                icon_data = None
                if icon_url:
                    response = requests.get(icon_url)
                    if response.status_code == 200:
                        icon_data = response.content
                
                await target.edit(
                    name=source.name,
                    icon=icon_data
                )
                print(f"{GREEN}[+] Guild Icon Changed: {source.name}{RESET}")
            except Exception as e:
                print(f"{RED}[-] Failed to clone server name/icon: {e}{RESET}")
            
            role_mapping = {}
            for role in reversed(source.roles):
                if role.name != "@everyone":
                    try:
                        new_role = await target.create_role(
                            name=role.name,
                            permissions=role.permissions,
                            color=role.color,
                            hoist=role.hoist,
                            mentionable=role.mentionable
                        )
                        role_mapping[role.id] = new_role
                        print(f"{GREEN}[+] Cloned Role: {role.name}{RESET}")
                    except Exception as e:
                        print(f"{RED}[-] Failed to create role {role.name}: {e}{RESET}")
            
            for category in source.categories:
                try:
                    if not isinstance(target, discord.Guild):
                        print(f"{RED}[-] Target is not a valid Guild object.{RESET}")
                        await client.close()
                        return

                    new_category = await target.create_category(
                        name=category.name,
                        position=category.position
                    )
                    print(f"{GREEN}[+] Created Category: {category.name}{RESET}")
                    for channel in category.channels:
                        try:
                            overwrites = {}
                            for target, permissions in channel.overwrites.items():
                                if isinstance(target, discord.Role):
                                    target_role = role_mapping.get(target.id)
                                    if target_role:
                                        overwrites[target_role] = permissions
                                elif isinstance(target, discord.Member):
                                    continue
                            
                            if isinstance(channel, discord.TextChannel):
                                new_channel = await new_category.create_text_channel(
                                    name=channel.name,
                                    topic=channel.topic,
                                    slowmode_delay=channel.slowmode_delay,
                                    overwrites=overwrites
                                )
                                print(f"{GREEN}[+] Cloned Text Channel: {channel.name}{RESET}")
                            elif isinstance(channel, discord.VoiceChannel):
                                new_channel = await new_category.create_voice_channel(
                                    name=channel.name,
                                    bitrate=channel.bitrate,
                                    user_limit=channel.user_limit,
                                    overwrites=overwrites
                                )
                                print(f"{GREEN}[+] Cloned Voice Channel: {channel.name}{RESET}")
                        except Exception as e:
                            print(f"{RED}[-] Failed to create channel {channel.name}: {e}{RESET}")
                except Exception as e:
                    print(f"{RED}[-] Failed to create category {category.name}: {e}{RESET}")
            
            print(f"{GREEN}Cloning completed!{RESET}")
        except Exception as e:
            print(f"{RED}[-] Error: {e}{RESET}")
        finally:
            await client.close()

    try:
        await client.start(token)
    except Exception as e:
        print(f"{RED}[-] Error: {e}{RESET}")
    finally:
        await client.close()

if __name__ == "__main__":
    main_menu()