async def initialize_db(pool):

	# Configuration table for guilds
	await pool.execute('''
					CREATE TABLE IF NOT EXISTS guildconfig(
						ID BIGINT PRIMARY KEY,
						mute_role BIGINT DEFAULT NULL,
						blind_role BIGINT DEFAULT NULL,
						log_channel BIGINT DEFAULT NULL,
						starboard_channel BIGINT DEFAULT NULL)
						''')

	# Long term mutes
	await pool.execute('''
					CREATE TABLE IF NOT EXISTS mutes(
						guild BIGINT NOT NULL,
						member BIGINT NOT NULL,
						mod BIGINT DEFAULT NULL,
						start_time BIGINT NOT NULL,
						end_time BIGINT NOT NULL,
						reason TEXT DEFAULT NULL)
						 ''')

	#Expels
	await pool.execute('''
					CREATE TABLE IF NOT EXISTS expelled(
						guild BIGINT NOT NULL,
						channel BIGINT NOT NULL,
						member BIGINT NOT NULL,
						mod BIGINT DEFAULT NULL,
						start_time BIGINT NOT NULL,
						end_time BIGINT NOT NULL,
						reason TEXT DEFAULT NULL)
						 ''')

	
	#Blinds
	await pool.execute('''
				CREATE TABLE IF NOT EXISTS blinded(
					guild BIGINT NOT NULL,
					member BIGINT NOT NULL,
					mod BIGINT DEFAULT NULL,
					start_time BIGINT NOT NULL,
					end_time BIGINT NOT NULL,
					reason TEXT DEFAULT NULL)
						''')