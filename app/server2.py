# Start daemon

# initialise counter at 1

# check feed intervals in DB

# get feeds which match current tick

# loop over feeds found

# ------

# spawn Worker(id, url, last_checked)

# check RSS url up (return error)

# check feed freshness, skip if not

# filter for new items since last check (timedelta)

# wait for write lock on DB

# write Posts items to DB

# update Feed last checked

# release write lock

# return new items Y/N code

# ------

# send websocket message with updated Feed IDs

# increment Tick

# wait $REFRESH minutes


# --------------------------------------------------
# startTick()
# incrementTick() ... 96 +> 1
# getTick()

