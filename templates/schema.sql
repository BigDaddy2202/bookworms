drop table if exists users;
create table users (
	user_id integer primary key autoincrement,
	username text NOT NULL,
	password text NOT NULL,
	name text NOT NULL,
	address text NOT NULL,
	email text NOT NULL,
	phone text NOT NULL
);

drop table if exists bookList;
create table bookList (
	book_id integer primary key autoincrement,
	book_name text NOT NULL
);

drop table if exists blogPosts;
create table blogPosts (
	post_id integer primary key autoincrement,
	title text NOT NULL,
	post_content text NOT NULL,
	post_time text NOT NULL,
	username text NOT NULL,
	img text NOT NULL,
	description text,
	user_id integer NOT NULL,
		FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

drop table if exists followers;
create table followers (
	follower_id integer primary key autoincrement,
	user_id_A integer NOT NULL,
	user_id_B integer NOT NULL,
	FOREIGN KEY (user_id_A, user_id_B) REFERENCES users (user_id, user_id) ON UPDATE CASCADE ON DELETE CASCADE
);

drop table if exists userbookList;
create table userBookList (
	book_id integer NOT NULL,
	user_id integer NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users (user_id) ON UPDATE CASCADE ON DELETE CASCADE
);

drop table if exists wishList;
create table wishlist (
	user_id integer NOT NULL,
	book_id integer NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users (user_id) ON UPDATE CASCADE ON DELETE CASCADE
	FOREIGN KEY (book_id) REFERENCES bookList (book_id) ON UPDATE CASCADE ON DELETE CASCADE
);
