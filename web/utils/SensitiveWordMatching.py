from urllib.parse import unquote

AttackDic = {
    "SQLi": ["'", '"', r'\\', r'/', '||', 'OR', 'AND', "SELECT", "UNION", "LIKE", "ALL", "NULL", "HEX"],
    "XSS": ["<script>", "</script>", "<iframe>", "</iframe>", 'SCRipt', 'SCRIPT', 'ScRIPt', 'SCRiPT', 'SCrIPT', 'SCriPT'
        , 'ScRIpT', 'ScRIPt', "<style>", "</style>", "<a>", "href", "`", "&#", " @[|\]^`"],
    "SSI": ['<!--#include file="', '"-->', '<!--#include+file', '"-->', '<!--#EXEC+cmd="', '"-->', '<!--#exec cmd="'],
    "CRLFi": ["Set-cookie:", "%0D%0A", "%E5%E98%8A", "%3D"],
    "XPath": ["<!--"],
    "LDAPi": ["^(#$!@#$)(()))******", ")("],
    "FormatString": ["%n", "%x", "%d"],
    "BufferOverflow": ["gets()", "scanf()", "strcat()", "sprintf()", "vsprintf()"]
}


def matchSensitiveWord(str):
    keys = list()
    for i in AttackDic.values():
        for j in i:
            if j in str:
                keys.append(j)
                continue
            if j in unquote(str):
                keys.append(j)
                continue
    return keys
