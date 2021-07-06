from .forms import BoardForm
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from .models import Board
from fcuser.models import Fcuser
from tag.models import Tag
# Create your views here.


def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')
    return render(request, 'board_detail.html', {'board': board})


def board_write(request):
    if not request.session.get('user'):
        return redirect('/fcuser/login/')

    if request.method == 'POST':  # 입력 내용을 DB에 저장해라.
        form = BoardForm(request.POST)  # POST일 땐 데이터를 넣음
        if form.is_valid():  # 필드값에 맞느 값들이 제대로 들어왔는지 확인하는 코드.입력값의 유효성 검사
            user_id = request.session.get('user')  # 사용자를 가져오기 위함.
            fcuser = Fcuser.objects.get(pk=user_id)

            tags = form.cleaned_data['tags'].split(',')

            board = Board()  # 모델 클래스 변수를 만들고 값을 채워넣어줌
            board.title = form.cleaned_data['title']
            # form으로 작성된 데이터중에서, 유효성 검사를 마친 데이터중에서, title이라는 데이터에 넣는다.
            board.contents = form.cleaned_data['contents']
            board.writer = fcuser  # 사용자는 session에 있음
            board.save()

            for tag in tags:
                if not tag:
                    continue

                _tag, _ = Tag.objects.get_or_create(name=tag)
                board.tags.add(_tag)

            return redirect('/board/list/')

    else:
        form = BoardForm()

    return render(request, 'board_write.html', {'form': form})


def board_list(request):
    all_boards = Board.objects.all().order_by('-id')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_boards, 2)

    boards = paginator.get_page(page)
    return render(request, 'board_list.html', {'boards': boards})
