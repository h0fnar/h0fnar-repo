import xbmc
import xbmcaddon
import xbmcgui
import os
import socket
import requests
import json
import commands


addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addon_dir = xbmc.translatePath( addon.getAddonInfo('path') )
icon_file = os.path.join(addon_dir, "resources", "images/")


try:
    if requests.get('http://ip-api.com/json').ok:
        html=requests.get('http://ip-api.com/json')
        parsed_json = json.loads(html.text)
        ip = (parsed_json['query'])
        country = (parsed_json['country'])
        current = country + "  " + ip
        current = "[COLOR lime]"+ "Current: " +current+ "[/COLOR]"
except:
    current = "[COLOR red]No Internet !!![/COLOR]"


rule_1 = addon.getSetting('rule_1')
rule_2 = addon.getSetting('rule_2')
rule_3 = addon.getSetting('rule_3')

ipaddress_1 = addon.getSetting('ipaddress_1')
ipaddress_2 = addon.getSetting('ipaddress_2')
ipaddress_3 = addon.getSetting('ipaddress_3')
ipaddress_bypass = addon.getSetting('ipaddress_bypass')

interface = addon.getSetting('interface')

if interface == "0":
    interface = "wlan0"
elif interface == "1":
    interface = "eth0"


def change_ip(ip):
    down = "ifconfig " + interface + " down"
    setip = "ifconfig " + interface + " " + ip
    up = "ifconfig " + interface + " up"
    os.system(str(down))
    os.system(str(setip))
    os.system(str(up))
    xbmc.sleep(3000)


host = commands.getoutput('ifconfig '+interface+' | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')


if host == ipaddress_bypass:
    ipaddress_bypass = ""
    current = "[COLOR red]Not Connected to VPN !!![/COLOR]"


dialog = xbmcgui.Dialog()
entries = [current]


if rule_1:
    rule_1 = "Connect VPN to: [COLOR cornflowerblue]" + rule_1 + "[/COLOR]"
    entries.append(rule_1)

if rule_2:
    rule_2 = "Connect VPN to: [COLOR cornflowerblue]" + rule_2 + "[/COLOR]"
    entries.append(rule_2)

if rule_3:
    rule_3 = "Connect VPN to: [COLOR cornflowerblue]" + rule_3 + "[/COLOR]"
    entries.append(rule_3)

if ipaddress_bypass:
    bypass_vpn = "[COLOR red]Disconnect VPN !!![/COLOR]"
    entries.append(bypass_vpn)
entries = filter(None, entries)


time = 10000


def get_geolocation():
    try:
        if requests.get('http://ip-api.com/json').ok:
            html=requests.get('http://ip-api.com/json')
            parsed_json = json.loads(html.text)
            ip = (parsed_json['query'])
            country = (parsed_json['country'])
            ccode = (parsed_json['countryCode'])
            message = "connected to " + country
            ip = "IP: " + ip
            icon = icon_file + ccode.lower() + ".png"
            return message, ip, icon
    except:
        message = "[COLOR red]No Internet !!![/COLOR]"
        ip = "Try another connection !!!"
        icon = icon_file + "danger.png"
        return message, ip, icon


nr = dialog.select("Select VPN Server", entries)

if nr==0:
    host = "Local ip: " + str(host)
    xbmcgui.Dialog().ok(addonname, current, host)

if ipaddress_1:
    if nr==1:
        change_ip(ipaddress_1)
        message, ip, icon = get_geolocation()
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(message, ip, time, icon))

if ipaddress_2:
    if nr==2:
        change_ip(ipaddress_2)
        message, ip, icon = get_geolocation()
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(message, ip, time, icon))

if ipaddress_3:
    if nr==3:
        change_ip(ipaddress_3)
        message, ip, icon = get_geolocation()
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(message, ip, time, icon))


number = len(entries) - 1
message_bypass = "[COLOR red]You are not connected to VPN !!![/COLOR]"

if ipaddress_bypass:
    if nr==number:
        change_ip(ipaddress_bypass)
        message, ip, icon = get_geolocation()
        icon = icon_file + "danger.png"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(message_bypass, ip, time, icon))


