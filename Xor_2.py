def xor_on_key(text,key):
    return "".join(chr(ord(v)^key)for v in text)
