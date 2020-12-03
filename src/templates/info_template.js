{
    "cert_info": {
        "owner": {{ cert.cert_owner() }},
        "subject": {{ cert.subject() }},
        "issuer": {{ cert.issuer() }},
        "validity": {{ cert.validity() }},
        "key_details": {{ cert.key_details() }}
    }
}
