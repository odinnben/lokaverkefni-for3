-- 0000000000000000000000000000000000000000000000000000000 PLACES 0000000000000000000000000000000000000000000000000000000 --

delimiter $$
drop procedure if exists AddPlace $$

create procedure AddPlace
(
	place_name varchar(75),
    place_region varchar(75),
    place_population int,
    web varchar(125),
    coord_lat double,
    coord_long double
)
begin
	declare coord_id int;
    
    set coord_id = null;
    if coord_lat is not null and coord_long is not null then
		insert into coordinates(latitude, longitude)values(coord_lat,coord_long);
        set coord_id = last_insert_id();
        commit;
	end if;
    
	insert into Places(placeName,coordinateID,region,population,webpage)
	values(place_name,coord_id,place_region,place_population,web);

    select last_insert_id();
end $$
delimiter ;


delimiter $$
drop procedure if exists PlaceList $$

create procedure PlaceList()
begin
	select placeName,region,webpage from Places order by PlaceName;
end $$
delimiter ;

delimiter $$
drop procedure if exists PlaceInfo $$

create procedure PlaceInfo(place_id int)
begin
	select P.placeName,P.region,P.population,P.webpage, C.latitude,C.longitude
    from Places P 
    left outer join Coordinates C on P.coordinateID = C.coordID
    where P.placeID = place_id;
end $$
delimiter ;

delimiter $$
drop procedure if exists UpdatePlace $$

create procedure UpdatePlace
(
	place_id int,
	place_name varchar(75),
    coordinate_id int,
    place_region varchar(75),
    place_population int,
    web varchar(125)
)
begin
	if coordinate_id is null then
		update Places
		set placeName = place_name ,region = place_region,population = place_population,webpage = web
		where placeID = place_id;
    else
		update Places
		set placeName = place_name,coordinateID = coordinate_id,region = place_region,population = place_population,webpage = web
		where placeID = place_id;
	end if;
    
    select row_count();
end $$
delimiter ;

delimiter $$
drop procedure if exists UpdatePlaceCoordinates $$

create procedure UpdatePlaceCoordinates(place_id int, coordinate_id int)
begin
	update Places set coordinateID = coordinate_id where placeID = place_id;
    
    select row_count();
end $$	
delimiter ;
	
delimiter $$
drop procedure if exists DeletePlace $$

create procedure DeletePlace(place_id int)
begin
	if not exists(select * from Districts where placeID = place_id) then
		delete from Places where placeID = place_id;
	end if;
    select row_count();
end $$
delimiter ;

-- 0000000000000000000000000000000000000000000000000000000 HOTELS 0000000000000000000000000000000000000000000000000000000 --

delimiter $$
drop procedure if exists AddHotel $$

create procedure AddHotel
(
    hotel_name varchar(75),
    street_address varchar(125),
    coord_lat double,
    coord_long double,
    hotel_manager varchar(75),
    hotel_webpage varchar(125),
    hotel_email varchar(85),
    hotel_phone varchar(15),
    district_id int
)
begin
	declare coord_id int;
    set coord_id = null;
    
    if coord_lat is not null and coord_long is not null then
		insert into coordinates(latitude, longitude)values(coord_lat,coord_long);
        set coord_id = last_insert_id();
        commit;
	end if;
    
	insert into Hotels(hotelName,streetAddress,coordinateID,manager,webpage,email,phone,districtID)
	values(hotel_name,street_address,coord_id,hotel_manager,hotel_webpage,hotel_email,hotel_phone,district_id);
    
    select last_insert_id();
end $$
delimiter ;

delimiter $$
drop procedure if exists HotelList $$

create procedure HotelList()
begin
	select H.hotelName,H.streetAddress,D.districtID,P.placeName,H.webpage
    from Hotels H
    inner join Districts D on H.districtID = D.districtID
    inner join Places P on D.placeID = P.placeID
    order by hotelName;
end $$
delimiter ;

delimiter $$
drop procedure if exists HotelInfo $$

create procedure HotelInfo(hotel_id int)
begin
	select H.hotelName,H.streetAddress,D.districtName,D.districtID,P.placeName,H.webpage,H.manager,H.email,H.phone,C.latitude,C.longitude
    from Hotels H
    inner join Districts D on H.districtID = D.districtID
    inner join Places P on D.placeID = P.placeID
    left outer join Coordinates C on H.coordinateID = C.coordID
    where H.hotelID = hotel_id;
end $$
delimiter ;

delimiter $$
drop procedure if exists UpdateHotel $$

create procedure UpdateHotel
(
	hotel_id int,
    hotel_name varchar(75),
    street_address varchar(125),
    coordinate_id int,
    hotel_manager varchar(75),
    hotel_webpage varchar(125),
    hotel_email varchar(85),
    hotel_phone varchar(15),
    district_id int
)
begin
	update Hotels set hotelName = hotel_name,streetAddress = street_address,coordinateID = coordinate_id,manager = hotel_manager,
                      webpage = hotel_webpage,email = hotel_email,phone = hotel_phone,districtID = district_id
	where hotelID = hotel_id;
    
    select row_count();
end $$
delimiter ;

delimiter $$
drop procedure if exists UpdateHotelCoordinates $$

create procedure UpdateHotelCoordinates(hotel_id int, coordinate_id int)
begin
	update Hotels set coordinateID = coordinate_id where hotelID = hotel_id;
    
    select row_count();
end $$	
delimiter ;

delimiter $$
drop procedure if exists DeleteHotel $$

create procedure DeleteHotel(hotel_id int)
begin
	call RemoveHotelMedia(hotel_id,null);
    commit;
	delete from Hotels where hotelID = hotel_id;
    
    select row_count();
end $$
delimiter ;

-- 000000000000000000000000000000000000000000000000000000 HOTEL MEDIA 000000000000000000000000000000000000000000000000000000 --

delimiter $$
drop procedure if exists AddHotelMedia $$

create procedure AddHotelMedia(hotel_id int,media_id int,media_url varchar(125))
begin
	insert into HotelMedia(hotelID,mediaID,url)values(hotel_id,media_id,media_url);
    
    select row_count();
end $$

delimiter ;

delimiter $$
drop procedure if exists HotelMediaList $$

create procedure HotelMediaList(hotel_id int)
begin
	select Hotels.hotelName,SocialMedia.mediaName,HotelMedia.url
    from Hotels
    inner join HotelMedia on Hotels.hotelID = HotelMedia.hotelID
    inner join SocialMedia on HotelMedia.mediaID = SocialMedia.mediaID
    and Hotels.hotelID = hotel_id;
end $$
delimiter $$

delimiter $$
drop procedure if exists RemoveHotelMedia $$

create procedure RemoveHotelMedia(hotel_id int, media_id int)
begin
	if media_id is null then
		delete from HotelMedia where hotelID = hotel_id;
	else
		delete from HotelMedia where hotelID = hotel_id and mediaID = media_id;
	end if;
    select row_count();
end $$
delimiter ;

-- 0000000000000000000000000000000000000000000000000000000 RESTAURANTS 000000000000000000000000000000000000000000000000000000 --

delimiter $$
drop procedure if exists AddRestaurant $$

create procedure AddRestaurant
(
	res_name varchar(75),
    res_type varchar(45),
    res_seats int,
    address varchar(125),
    coord_lat double,
    coord_long double,
    res_manager varchar(75),
    web varchar(125),
    res_phone varchar(15),
    district_id int
)
begin
	declare coord_id int;
    
    set coord_id = null;
    if coord_lat is not null and coord_long is not null then
		insert into coordinates(latitude, longitude)values(coord_lat,coord_long);
        set coord_id = last_insert_id();
        commit;
	end if;
    
    insert into Restaurants(restaurantName,restaurantType,capacity,streetAddress,coordinateID,manager,webpage,phone,districtID)
    values(res_name,res_type,res_seats,address,coord_id,res_manager,web,res_phone,district_id);
    
    select last_insert_id();
end $$
delimiter ;

delimiter $$
drop procedure if exists RestaurantList $$

create procedure RestaurantList()
begin
	select R.restaurantName,R.streetAddress,D.districtID,D.districtName,R.phone
    from Restaurants R
    inner join Districts D on R.districtID = D.districtID order by R.restaurantName;
end $$
delimiter ;

delimiter $$
drop procedure if exists RestaurantInfo $$

create procedure RestaurantInfo(restaurant_id int)
begin
	select R.restaurantName,R.streetAddress,D.districtID,D.districtName,R.restaurantType,R.capacity,R.phone,R.webpage,R.manager,C.latitude,C.longitude
    from Restaurants R  
    inner join Districts D on R.districtID = D.districtID
    left outer join Coordinates C on R.coordinateID = C.coordID
    where R.restaurantID = restaurant_id;
end $$
delimiter ;

delimiter $$
drop procedure if exists UpdateRestaurant $$

create procedure UpdateRestaurant
(
	restaurant_id int,
	res_name varchar(75),
    res_type varchar(45),
    res_seats int,
    address varchar(125),
    coord_id int,
    res_manager varchar(75),
    web varchar(125),
    res_phone varchar(15),
    district_id int
)
begin
	update Restaurants
    set restaurantName = res_name,restaurantType = res_type,capacity = res_seats,streetAddress = address,
        coordinateID = coord_id,manager = res_manager,webpage = web,phone = res_phone,districtID = district_id
	where restaurantID = restaurant_id;
    
    select row_count();
end $$
delimiter ;

delimiter $$
drop procedure if exists DeleteRestaurant $$

create procedure DeleteRestaurant(restaurant_id int)
begin
	call RemoveRestaurantMedia(restaurant_id,null);
    delete from Restaurants where restaurantID = restaurant_id;
    
    select row_count();
end $$
delimiter ;

-- 0000000000000000000000000000000000000000000000000000 RESTAURANT MEDIA 0000000000000000000000000000000000000000000000000000 --

delimiter $$
drop procedure if exists AddRestaurantMedia $$

create procedure AddRestaurantMedia(restaurant_id int,media_id int,media_url varchar(125))
begin
	insert into RestaurantMedia(restaurantID,mediaID,url)values(restaurant_id,media_id,media_url);
    
    select row_count();
end $$

delimiter ;

delimiter $$
drop procedure if exists RestaurantMediaList $$

create procedure RestaurantMediaList(restaurant_id int)
begin
	select Restaurants.restaurantName,SocialMedia.mediaName,RestaurantMedia.url
    from Restaurants
    inner join RestaurantMedia on Restaurants.restaurantID = RestaurantMedia.restaurantID
    inner join SocialMedia on RestaurantMedia.mediaID = SocialMedia.mediaID
    and Restaurants.restaurantID = restaurant_id;
end $$
delimiter $$

delimiter $$
drop procedure if exists RemoveRestaurantMedia $$

create procedure RemoveRestaurantMedia(restaurant_id int, media_id int)
begin
	if media_id is null then
		delete from RestaurantMedia where restaurantID = restaurant_id;
	else
		delete from RestaurantMedia where restaurantID = restaurant_id and mediaID = media_id;
	end if;
    select row_count();
end $$
delimiter ;

-- 0000000000000000000000000000000000000000000000000000000 ACTIVITIES 0000000000000000000000000000000000000000000000000000000 --

delimiter $$
drop procedure if exists AddActivity $$

create procedure AddActivity
(
	activity_name varchar(75),
    activity_company varchar(75),
    web varchar(125),
    district_id int
)
begin
	insert into Activities(activityName,company,webpage,districtID)
    values(activity_name,activity_company,web,district_id);
    
    select last_insert_id();
end $$
delimiter ;

delimiter $$
drop procedure if exists ActivityList $$

create procedure ActivityList()
begin
	select activityID, activityName, company 
    from Activities
    order by activityName;
end $$
delimiter ;

delimiter $$
drop procedure if exists ActivityInfo $$

create procedure ActivityInfo(activity_id int)
begin
	select A.activityID, A.activityName, A.company, P.placeName, A.webpage
    from Activities A
    inner join Districts D on A.districtID = D.districtID
    inner join Places P on D.placeID = P.placeID
    and A.activityID = activity_id;
end $$
delimiter ;

delimiter $$
drop procedure if exists UpdateActivity $$

create procedure UpdateActivity
(
	activity_id int,
	activity_name varchar(75),
    activity_company varchar(75),
    web varchar(125),
    district_id int
)
begin
	update Activities
    set activityName = activity_name,company = activity_company,webpage = web,districtID = district_id
    where activityID = activity_id;
    
    select row_count();
end $$
delimiter ;

delimiter $$
drop procedure if exists DeleteActivity $$

create procedure DeleteActivity(activity_id int)
begin
	call RemoveActivityMedia(activity_id,null);
    delete from Activities where activityID = activity_id;
    
    select row_count();
end $$
delimiter ;

-- 00000000000000000000000000000000000000000000000000000 ACTIVITY MEDIA 00000000000000000000000000000000000000000000000000000 --

delimiter $$
drop procedure if exists AddActivityMedia $$

create procedure AddActivityMedia(activity_id int,media_id int,media_url varchar(125))
begin
	insert into ActivityMedia(activityID,mediaID,url)values(activity_id,media_id,media_url);
    
    select row_count();
end $$

delimiter ;

delimiter $$
drop procedure if exists ActivityMediaList $$

create procedure ActivityMediaList(activity_id int)
begin
	select Activities.activityName,SocialMedia.mediaName,ActivityMedia.url
    from Activities
    inner join ActivityMedia on Activities.activityID = ActivityMedia.activityID
    inner join SocialMedia on ActivityMedia.mediaID = SocialMedia.mediaID
    and Activities.activityID = activity_id;
end $$
delimiter $$

delimiter $$
drop procedure if exists RemoveActivityMedia $$

create procedure RemoveActivityMedia(activity_id int, media_id int)
begin
	if media_id is null then
		delete from ActivityMedia where activityID = activity_id;
	else
		delete from ActivityMedia where activityID = activity_id and mediaID = media_id;
	end if;
    select row_count();
end $$
delimiter ;

-- 00000000000000000000000000000000000000000000000000000 COORDINATES 0000000000000000000000000000000000000000000000000000 --
delimiter $$
drop procedure if exists AddCoordinates $$

create procedure AddCoordinates(coord_lat double, coord_long double)
begin
	insert into Coordinates(latitude,longitude)values(coord_lat,coord_long);
    select last_insert_ID();
end $$
delimiter ;

delimiter $$
drop procedure if exists UpdateCoordinates $$

create procedure UpdateCoordinates(coordinate_id int,hotel_latitude double, hotel_longitude double)
begin
	update Coordinates
    set latitude = hotel_latitude,longitude = hotel_longitude
    where coordID = coordinate_id;

    select row_count();
end $$
delimiter ;


-- 000000000000000000000000000000000000000000000000000000 SOCIAL MEDIA 000000000000000000000000000000000000000000000000000000 --

delimiter $$
drop procedure if exists AddSocialMedia $$

create procedure AddSocialMedia(media_name varchar(75), default_page varchar(125))
begin
	insert into SocialMedia(mediaName,defaultPage)values(media_name,default_page);
    
    select row_count();
end $$
delimiter ;

delimiter $$
drop procedure if exists SocialMediaList $$

create procedure SocialMediaList()
begin
	select mediaID, mediaName,defaultPage from SocialMedia;
end $$
delimiter ;

delimiter $$
drop procedure if exists SocialMediaInfo $$

create procedure SocialMediaInfo(media_id int)
begin
	select mediaID, mediaName,defaultPage from SocialMedia where mediaID = media_id;
end $$
delimiter ;

delimiter $$
drop procedure if exists UpdateSocialMedia $$

create procedure UpdateSocialMedia(media_id int, media_name varchar(75), default_page varchar(125))
begin
	update SocialMedia
    set mediaName = media_name,defaultPage = default_page
    where mediaID = media_id;
    
    select row_count();
end $$
delimiter ;

delimiter $$
drop procedure if exists DeleteSocialMedia $$

create procedure DeleteSocialMedia(media_id int)
begin
	delete from SocialMedia where mediaID = media_id;
    
    select row_count();
end $$
delimiter ;

-- 000000000000000000000000000000000000000000000000000000 ÝMISLEGT 000000000000000000000000000000000000000000000000000000 --

delimiter $$
drop function if exists NumberOfDistrictHotels $$

create function NumberOfDistrictHotels(district_id int) 
returns int
begin
	return(select count(*) from Hotels where districtID = district_id);
end $$
delimiter ;

delimiter $$
drop function if exists TotalNumberOfHotels $$

create function TotalNumberOfHotels() 
returns int
begin
	return(select count(*) from Hotels);
end $$
delimiter ;