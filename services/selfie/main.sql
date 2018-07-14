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
    "199f5f2ea963323178210a676b6e9029",
    "1994-07-17",
    "male",
    "The Owner is too lazy to left anything",
    1531474333
);
