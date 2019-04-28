from decorators import login_required


@login_required
def get_error(request):
    raise Exception('Some exception text')

