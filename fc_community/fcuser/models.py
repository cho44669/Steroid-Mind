from django.db import models

# Create your models here.
# 클래스를 만들 때 장고에서 제공하고 있는 models.Model을 상속 받아야함


class Fcuser(models.Model):
    username = models.CharField(max_length=32,
                                verbose_name='사용자명')  # 유저네임이라는 필드를 만들었고, 관리자 페이지에서 username 사용자명이라고 뜸.
    useremail = models.EmailField(max_length=128,       # Email 필드는 문자열이 이메일형태의 검증까지해줌.(템플릿에서 useremail 타입='eamil'까지 해줘야함.)
                                  verbose_name='사용자이메일')
    password = models.CharField(max_length=64,
                                verbose_name='비밀번호')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='등록시간')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'fastcampus_fcuser'
        verbose_name = '패스트캠퍼스 사용자'
        verbose_name_plural = '패스트캠퍼스 사용자'
