from worker import mappings


def convert(items):
    def do(value):
        return mappings.get('schema', value)(value).to_native()
    return [do(val) for val in items] if isinstance(items, list) else do(items)
