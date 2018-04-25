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
create procedure addUser(
	nn varchar(40),
    lo varchar(40),
    an boolean
)
begin
	insert into notendur values(nn,lo,an);
    select row_count();
end //

create procedure delUser(
	nn varchar(40)
)
begin
	delete from notendur where notendanafn = nn;
    select row_count();
end //

create procedure updateUserPass(
	nn varchar(40),
    lo varchar(40)
)
begin
	update notendure set lykilord = lo where notendanafn = nn;
    select row_count();
end //

create procedure updateUserAdmin(
	nn varchar(40),
    an boolean
)
begin
	update notendure set admin = an where notendanafn = nn;
    select row_count();
end //

create procedure listUsers()
begin
	select notendanafn,admin from notendur;
end //
delimiter **