use 1501002670_icelandinfo;

drop table if exists notendur;
create table notendur(
	notendanafn varchar(40) primary key,
    lykilord varchar(40),
    admin boolean default False
);

insert into notendur values
	('Odinn','12345',False),
	('Matti','12345',True)
;

delimiter //
drop procedure if exists addUser //
create procedure addUser(
	nn varchar(40),
    lo varchar(40),
    an boolean
)
begin
	insert into notendur values(nn,lo,an);
    select row_count();
end //

drop procedure if exists delUser //
create procedure delUser(
	nn varchar(40)
)
begin
	delete from notendur where notendanafn = nn;
    select row_count();
end //

drop procedure if exists updateUserPass //
create procedure updateUserPass(
	nn varchar(40),
    lo varchar(40)
)
begin
	update notendur set lykilord = lo where notendanafn = nn;
    select row_count();
end //

drop procedure if exists updateUserAdmin //
create procedure updateUserAdmin(
	nn varchar(40),
    an boolean
)
begin
	update notendur set admin = an where notendanafn = nn;
    select row_count();
end //

drop procedure if exists listUsers //
create procedure listUsers()
begin
	select notendanafn,admin from notendur;
end //
delimiter **
