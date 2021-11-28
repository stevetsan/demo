## Q1
SQL query statement work on MySQL 5.7 located at [here](./q1.sql)

## Q2
Sample of the (tab separated) access logfile located [here](./q2/cdn_access_log.txt)

Python(3.8) file for calculating the total data transfer for JPEG files from 24th Aug to 25th Aug is located [here](./q2/q2.py)<br/>
You may run it directly with Python 3.8 or by the Dockerfile located [here](./q2/Dockerfile)

## Q3
### Database selection and design
I will prefer using AWS Aurora Serverless for such use case. 
Theoretically, user are likely to react most rapidly at the beginning of the launch of vote, <br/>
however I believe it is hard to predict number of traffic and where the spike will happen. 

Which with traditional AWS RDS, the capacity adjustments would be time-consuming moreover hard to execute. <br/>
Even though, when it comes to cost per hour, Serverless would be more expensive compare to RDS with equivalent computing power.<br/>
But for such an ad hoc task with unpredictable traffic spikes and mostly short runtime, I believe Aurora Serverless could be a good fit.


In production case, I assume there are at least 3 Table:
1. **Candidate Table**: Storing candidate's id, name and other personal information
```
id INTEGER,
name VARCHAR(256),
...
```
2. **User Table**: Storing front end user's id, name and other personal information
```
id INTEGER,
name VARCHAR(256),
...
```
3. **Voting Table**: Storing which user had vote to which candidate along with vote time, opinion and other information
```
id INTEGER,
created_at TIMESTAMP,
candidate_id INTEGER,
opinion TEXT,
...
```

### RESTful api
I will prefer to use AWS Lambda to host the api over AWS ECS since:
- The api handle relatively simple action as below, which allow us to fit within the limits that Lambda enforces
  - Handle POST request by consuming a json payload
  - Handle GET request by returning the result in a json format
- Lambda provide a compelling hands-off solution to a highly scalable application

As to handle the dramatic increase for both POST and GET request, if immediacy of the data can be compromised.<br/>
Alternatively, I will suggest rather than using Aurora Serverless, we may use AWS RDS with below adjustment.<br/>
for handle POST request:
- push all the POST request from API to a message queue (AWS SQS)
- Handle the insert query with a separate lambda function which consume from the message queue

for handle GET request:
- Use cache-aside strategy provide by Amazon ElastiCache for Redis on top of a MySQL

By limiting the insert action per second with lambda and prevent executing the same query for result directly from the DB, 
we may limit and minimized the stress on the DB and eventually set up the DB with RDS for a desirable capacity.


### Demo
Dockerfile is located [here](./q3/Dockerfile)<br/>
The Dockerfile run `script.sh` which execute 2 python file
- [database/db_init.py](./q3/database/db_init.py): set up an embedded database - sqlite within the container with 2 table
  - candidate: Candidate Table mention [above](#database-selection-and-design)
  - vote: Voting Table mention [above](#database-selection-and-design)<br/>
    _(I assume the front end will hard code the candidate list with its candidate_id,
    so in the demo the RESTful api will communicate with candidate_id)_
- [app.py](./q3/app.py): set up a RESTFul API by flask with 2 endpoint
  - handle POST request with input for the candidate_id and opinion (optional)
  - handle GET request which will return cumulative vote count for each candidate and total number of vote for all candidate in last 10 minutes

### Setup for the Demo
Build the image by `docker build -t q3 . `<br/>
Run the image by `docker run -d -p 5000:5000 q3`

The flask api will be hosted on http://0.0.0.0:5000/

Then you may run the [sample_request.py](./q3/sample_request.py) at local<br/>
Which will generate 3 POST request to http://0.0.0.0:5000/vote/ with below json payload:
- `{'candidate_id': 2}` : it will return `{'success': True}`, since the field opinion is optional
- `{'candidate_id': 2, 'opinion': 'test'}`: it will return `{'success': True}`
- `{'opinion': 'test'}` : it will return `{'success': False, "error_message": "candidate_id is required!"}`

And a GET request to http://0.0.0.0:5000/result/ which will return a list of 2 list:
- `[{"candidate_id": int, "num_vote": int}]`: list of dict contain the number of vote for each candidate
- `[{"total_vote_10_min": int}]`: Total number of vote for all candidate in last 10 minutes

Or you may directly run below in terminal<br/>
POST without "opinion"
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"candidate_id": 2}' \
  http://0.0.0.0:5000/vote/
```
POST with "opinion"
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"candidate_id": 2, "opinion": "test"}' \
  http://0.0.0.0:5000/vote/
```
GET
```
curl --header "Content-Type: application/json" \
  --request GET \
  http://0.0.0.0:5000/result/
```