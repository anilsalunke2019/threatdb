# -*- coding: utf-8 -*-
"""
All the JSON endpoints from where raw data is being fetched
Created on 10/9/2019
@author: Anurag
"""

# add the future endpoint without hostname like below
ip_targets = [
    '/apacheParser.php',
    '/badguysParser.php',
    '/badipsParser.php',
    '/bruteForceLoginParser.php',
    '/emergingThreatsParser.php',
    '/feodoParser.php',
    '/ftpParser.php',
    '/greenSnowParser.php',
    '/imapParser.php',
    '/mailParser.php',
    '/otxParser.php',
    '/sipParser.php',
    '/strongipsParser.php',
    '/sshParser.php',
    '/osintParser.php',
    '/botsParser.php',

]

url_targets = [
    '/malware_url/crdfParser.php',
    '/malware_url/blocklistParser.php',
    '/malware_url/urlhausParser.php',
    '/malware_url/MDLParser.php',
    '/malware_url/dshieldLowParser.php',
    '/malware_url/dshieldMediumParser.php',
    '/malware_url/dshieldHighParser.php',
    '/ransomware/blocklistParser.php',
]

"""
Challanges:
    1. Currently we are fetching data from the following sources. 
        Every source has its own policy and IP block listing period.
    2. Variable duration of keeping the IP address block by each data source providers.

    https://lists.blocklist.de/lists/apache.txt                         -- last 48 hours
    http://cinsscore.com/list/ci-badguys.txt                            -- unknown
    https://www.badips.com/get/list/any/2                               -- unknown
    https://lists.blocklist.de/lists/bruteforcelogin.txt                -- last 48 hours
    https://rules.emergingthreats.net/blockrules/compromised-ips.txt    -- unknown
    https://feodotracker.abuse.ch/downloads/ipblocklist.csv             -- last 30 days   Extra info
    https://lists.blocklist.de/lists/ftp.txt                            -- last 48 hours
    http://blocklist.greensnow.co/greensnow.txt                         -- manual
    https://lists.blocklist.de/lists/imap.txt                           -- last 48 hours
    https://lists.blocklist.de/lists/ircbot.txt                         -- last 48 hours
    https://lists.blocklist.de/lists/mail.txt                           -- last 48 hours
    https://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt      -- unknown         Extra info
    https://lists.blocklist.de/lists/sip.txt                            -- last 48 hours
    https://lists.blocklist.de/lists/ssh.txt                            -- last 48 hours
    https://lists.blocklist.de/lists/strongips.txt                      -- last 48 hours
    https://threatcenter.crdf.fr/public/urls/last_malicious_websites.txt -- manual         URL  EXTRA INFO
    https://blocklist.site/app/dl/malware                               -- 6 months        URL  NO EXTRA INFO
    https://urlhaus-api.abuse.ch/v1/urls/recent/                        -- last 30 days    URL JSON
    http://www.malwaredomainlist.com/mdlcsv.php                         -- unknown         URL CSV
    https://www.dshield.org/feeds/suspiciousdomains_High.txt            -- 6 months        URL  EXTRA INFO
    https://secure.dshield.org/feeds/suspiciousdomains_Low.txt          -- 6 months        URL  EXTRA INFO 
    https://www.dshield.org/feeds/suspiciousdomains_Medium.txt          -- 6 months        URL  EXTRA INFO 
    https://blocklist.site/app/dl/ransomware                            -- 6 months        URL  NO EXTRA INFO 
"""
