drop database if exists 1501002670_IcelandInfo;
create database 1501002670_IcelandInfo
	default character set utf8
    default collate utf8_general_ci;
set default_storage_engine = innodb;
set sql_mode = 'STRICT_ALL_TABLES';

use 1501002670_IcelandInfo;

create table Coordinates
(
	coordID int auto_increment,
    latitude double,
    longitude double,
    constraint coordinateID primary key(coordID),
    constraint coord_NQ unique(latitude,longitude)
);

create table SocialMedia
(
	mediaID int auto_increment,
    mediaName varchar(75) not null,
    defaultPage varchar(125),
    constraint media_PK primary key(mediaID)
);

create table Places
(
    placeID int auto_increment,
    placeName varchar(75) not null,
    coordinateID int null,
    region varchar(75),			-- Höfuðborgarsvæðið, Norðurland o.s.frv.
    population int,
    webpage varchar(125),
    constraint place_PK primary key(placeID),
    constraint place_coordinates_FK foreign key(coordinateID) references Coordinates(coordID)
);

create table Districts
(
	districtID int,				-- hér má nota íslensku póstnúmerin.
    districtName varchar(75) not null,
    placeID int not null,
    constraint district_PK primary key(districtID),
    constraint district_place_FK foreign key(placeID) references Places(placeID)
);

create table Hotels
(
    hotelID int auto_increment,
    hotelName varchar(75) not null,
    streetAddress varchar(125),
    coordinateID int null,
    manager varchar(75),
    webpage varchar(125),
    email varchar(85),
    phone varchar(15),
    districtID int,
    constraint hotel_PK primary key(hotelID),
    constraint hotel_district_FK foreign key(districtID) references Districts(districtID),
    constraint hotel_coordinates_FK foreign key(coordinateID) references Coordinates(coordID)
);

create table HotelMedia
(
	hotelID int not null,
    mediaID int not null,
    url varchar(125) not null,
    constraint hotelmedia_PK primary key(hotelID,mediaID),
    constraint hotelmedia_hotel_FK foreign key(hotelID) references Hotels(hotelID),
    constraint hotelmedia_media_FK foreign key(mediaID) references SocialMedia(mediaID)    
);

create table Restaurants
(
    restaurantID int auto_increment,
    restaurantName varchar(75),
    restaurantType varchar(45),		-- franskur, indverskur, ítalskur o.s.frv.
    capacity int not null,			-- hámarksfjöldi gesta
    streetAddress varchar(125),
    coordinateID int null,
    manager varchar(75),
    webpage varchar(125),
    phone varchar(15),
    districtID int,
    constraint restaurant_PK primary key(restaurantID),
    constraint restaurant_district_FK foreign key(districtID) references Districts(districtID),
    constraint restaurant_coordinates_FK foreign key(coordinateID) references Coordinates(coordID)
);

create table RestaurantMedia
(
	restaurantID int not null,
    mediaID int not null,
    url varchar(125) not null,
    constraint restaurantmedia_PK primary key(restaurantID,mediaID),
    constraint restaurantmedia_restaurant_FK foreign key(restaurantID) references Restaurants(restaurantID),
    constraint restaurantmedia_media_FK foreign key(mediaID) references SocialMedia(mediaID)    
);

create table Activities
(
    activityID int not null auto_increment,
    activityName varchar(75),
    company varchar(75),
    webpage varchar(125),
    districtID int,
    constraint activity_PK primary key(activityID),
    constraint activity_district_FK foreign key(districtID) references Districts(districtID)
);

create table ActivityMedia
(
	activityID int not null,
    mediaID int not null,
    url varchar(125) not null,
    constraint activitymedia_PK primary key(activityID,mediaID),
    constraint activitymedia_activity_FK foreign key(activityID) references Activities(activityID),
    constraint activitymedia_media_FK foreign key(mediaID) references SocialMedia(mediaID)    
);