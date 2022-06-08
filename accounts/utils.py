class ResponseInfo(object):
    def __init__(self, user=None, **args):
        self.response = {
            "status": args.get('status', 200),
            "data": args.get('data', []),
            "message": args.get('message', 'success')
        }