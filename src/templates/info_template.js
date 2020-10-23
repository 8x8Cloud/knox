{
    "cert_info": {
        "subject": {{ cert.subject() }},
        "issuer": {{ cert.issuer() }},
        "validity": {{ cert.validity() }},
        "key_details": {{ cert.key_details() }}
    }
}
