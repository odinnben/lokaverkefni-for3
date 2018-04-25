insert into SocialMedia(mediaName,defaultPage)values('Facebook','https://www.facebook.com/');
insert into SocialMedia(mediaName,defaultPage)values('Twitter','https://twitter.com/');
insert into SocialMedia(mediaName,defaultPage)values('Instagram','https://www.instagram.com/');  
insert into SocialMedia(mediaName,defaultPage)values('Snapchat','https://www.snapchat.com/');
insert into SocialMedia(mediaName,defaultPage)values('Youtube','https://www.youtube.com/');
insert into SocialMedia(mediaName,defaultPage)values('Wikipedia','https://www.wikipedia.org/');


insert into Coordinates(latitude,longitude)values('64.135338','-21.89521');			-- Reykjavík
insert into Coordinates(latitude,longitude)values('65.683868','-18.11046');			-- Akureyri
insert into Coordinates(latitude,longitude)values('65.2668743','-14.3948469'); 		-- Egilsstaðir


insert into Places(placeName,coordinateID,region,population,webpage)values('Reykjavík',1,'Höfuðborgarsvæðið',123246,'https://reykjavik.is/');
insert into Places(placeName,coordinateID,region,population,webpage)values('Akureyri',2,'Norðurland',18488,'https://www.akureyri.is/');
insert into Places(placeName,coordinateID,region,population,webpage)values('Egilsstaðir',3,'Austurland',2306,'https://www.fljotsdalsherad.is/');


insert into Districts(districtID,districtName,placeID)values(101,'Miðbærinn',1);
insert into Districts(districtID,districtName,placeID)values(103,'Háaleitis- og Bústaðahverfi',1);
insert into Districts(districtID,districtName,placeID)values(104,'Laugardalur',1);
insert into Districts(districtID,districtName,placeID)values(105,'Hlíðar',1);
insert into Districts(districtID,districtName,placeID)values(107,'Vesturbær',1);
insert into Districts(districtID,districtName,placeID)values(108,'Háaleitis- og Bústaðahverfi',1);
insert into Districts(districtID,districtName,placeID)values(109,'Breiðholt',1);
insert into Districts(districtID,districtName,placeID)values(110,'Árbær',1);
insert into Districts(districtID,districtName,placeID)values(111,'Breiholt',1);
insert into Districts(districtID,districtName,placeID)values(112,'Grafarvogur',1);
insert into Districts(districtID,districtName,placeID)values(113,'Grafarholt og Úlfarsárdalur',1);
insert into Districts(districtID,districtName,placeID)values(116,'Kjalarnes',1);
insert into Districts(districtID,districtName,placeID)values(600,'Þéttbýli',2);
insert into Districts(districtID,districtName,placeID)values(601,'Dreifbýli',2);
insert into Districts(districtID,districtName,placeID)values(700,'Þéttbýli',3);
insert into Districts(districtID,districtName,placeID)values(701,'Dreifbýli',3);


insert into Hotels(hotelName,streetAddress,coordinateID,manager,webpage,email,phone,districtID)
values('Centerhotel Plaza','Aðalstræti 4',null,'Ingibjörg K. Sigurjónsdóttir','https://www.centerhotels.com/',null,'354-5958500',101);
insert into Hotels(hotelName,streetAddress,coordinateID,manager,webpage,email,phone,districtID)
values('Hotel Cabin','Borgartún 32',null,null,'http://hotelcabin.is/','booking@hotelcabin.is','354-5116030',105);
insert into Hotels(hotelName,streetAddress,coordinateID,manager,webpage,email,phone,districtID)
values('Hótel KEA','Hafnarstraeti 87-89',null,null,'https://www.keahotels.is/en/hotels/hotel-kea','kea@keahotels.is','354-4602000',600);
insert into Hotels(hotelName,streetAddress,coordinateID,manager,webpage,email,phone,districtID)
values('Hótel Valaskjálf','Skógarlöndum 3',null,null,'http://www.valaskjalf.is/index.php/is/','701hotels@701hotels.is','354-4711600',700);


insert into HotelMedia(hotelID,mediaID,url)values(1,1,'https://www.facebook.com/CenterHotels/');				-- Center hotels
insert into HotelMedia(hotelID,mediaID,url)values(1,2,'https://twitter.com/CenterHotels');						-- Center hotels
insert into HotelMedia(hotelID,mediaID,url)values(2,1,'https://www.facebook.com/hotelcabin');					-- Hotel Cabin
insert into HotelMedia(hotelID,mediaID,url)values(4,1,'https://www.facebook.com/valaskjalfegilsstadir/');		-- Hotel Valaskjálf