def get_regulation_dict():
    regs = get_all()
    result = {}
    for r in regs:
        try:
            result[r.key] = json.loads(r.value)
        except:
            result[r.key] = r.value
    return result
