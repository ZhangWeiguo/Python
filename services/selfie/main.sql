create database selfie;
use selfie;
create table user_info(
    user_name   varchar(24) primary key,
    pass_word   varchar(64) not null,
    birth       varchar(32),
    sex         enum('male','female',''),
    about_me    text,
    create_time bigint
)
default charset = 'utf8'
engine = innodb; 

insert into user_info values(
    "NoTeethSmallPerson",
    "0804835823445a2a03b34187adac1440",
    "1994-07-17",
    "male",
    "The Owner is too lazy to left anything",
    1531474333
);


create table blog_cate(
    cate                varchar(256) not null,
    sub_cate            varchar(256) not null,
    cate_position       int not null,
    sub_cate_position   int not null
)
default charset = 'utf8'
engine = innodb;


insert into blog_cate values 
("理想","算法",1,1),
("理想","架构",1,2),
("理想","前端",1,3),
("理想","随笔",1,4),
("生活","风景",2,1),
("生活","随笔",2,2);


create table blog_info(
    blog_id     bigint primary key auto_increment,
    user_name   varchar(24) not null,
    title       varchar(256) not null,
    abstract    text,
    content     text,
    create_time bigint,
    cate        varchar(256) not null,
    sub_cate    varchar(256) not null
)
default charset = 'utf8'
engine = innodb; 


insert into blog_info(
    user_name,title,abstract,content,create_time,cate,sub_cate
) values
(
    "NoTeethSmallPerson",
    "青玉案 元夕",
    "辛弃疾",
    "东风夜放花千树。更吹落、星如雨。宝马雕车香满路。凤箫声动，玉壶光转，一夜鱼龙舞。蛾儿雪柳黄金缕。笑语盈盈暗香去。众里寻他千百度。蓦然回首，那人却在，灯火阑珊处。",
    1531549659,
    "生活",
    "随笔"
);


create table comment_info(
    comment_id  bigint primary key auto_increment,
    content     text not null,
    user_name   varchar(24) not null,
    blog_id     bigint not null,
    create_time bigint
)
default charset = 'utf8'
engine = innodb;