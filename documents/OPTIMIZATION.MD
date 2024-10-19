## n+1

The n+1 problem in databases is a common performance issue that occurs when an application makes n+1 queries to retrieve related data, rather than retrieving all necessary data in a single or more efficient query. This typically arises in object-relational mapping (ORM) frameworks, like Django’s ORM, Hibernate, or SQLAlchemy, where an initial query fetches a set of records, but then each record triggers another query to fetch related data

#### What Causes the N+1 Problem?

Typically, the problem arises when we

Query a list of parent records (e.g., courses).
For each record in that list, issue a separate query to retrieve related child records (e.g., instructors).

This results in one initial query plus n additional queries for each related record, leading to n+1 queries, where n is the number of parent records.

### Example

```py
class Instructor(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    title = models.CharField(max_length=100)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

```

```py
courses = Course.objects.all()
for course in courses:
    print(course.instructor.name)

```

```sql
SELECT * FROM course
```

1. select every thing from course mode
2. now, let's say for each course there is 10 instructors, we need to make 10 additional queries (1+10) = 11.

Executing multiple queries is slower than retrieving all data in one efficient query

## Solving the N+1 Problem

depending on the types of relationship, we can use `select_ralated()` or `prefectch_releate()`.

#### 1. select_related()

- Used for single-valued relationships (ForeignKey or OneToOneField).
- It performs a JOIN and fetches the related data in a single query.

```py
courses = Course.objects.select_related('instructor')
```

Now, only one query.

```sql
SELECT course.*, instructor.* FROM course
INNER JOIN instructor ON course.instructor_id = instructor.id;
```

#### 2. 2. prefetch_related:

- Used for multi-valued relationships (ManyToManyField or reverse ForeignKey).
- Fetches related data in separate queries, but the ORM handles the relationships efficiently to avoid the n+1 problem.

```py
courses = Course.objects.prefetch_related('students')
```

This performs 2 queries (one for courses and one for related students):

```sql
SELECT * FROM course;
SELECT * FROM student WHERE course_id IN (list of course IDs);
```

This prevents the n+1 problem by batching the retrieval of related data.

#### General Solutions to Avoid N+1 Problem:

Eager Loading: Use select_related and prefetch_related to load related data in advance.
Batch Fetching: In some systems, we can batch-fetch related data to avoid issuing one query per parent record.
Optimize Queries: Analyze our queries using tools like Django’s django-debug-toolbar to identify potential n+1 problems and optimize accordingly.

### Foreign key

a ForeignKey is used to establish a many-to-one relationship between two models. For example, a Course might have a single Instructor, but one Instructor can have multiple Course objects.

```py

class Instructor(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    title = models.CharField(max_length=100)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="courses")
```

- Instructor is the model being referenced `(the "one" side)`.
- Course is the model that holds the ForeignKey `(the "many" side)`.

#### What is a Reverse ForeignKey?

The reverse ForeignKey is when we want to access all the related objects (e.g., all courses) from the other side of the relationship (e.g., from the instructor's perspective).

we can change the default name (course_set) by providing a related_name in the ForeignKey definition:

#### Why "Reverse"?

The term "reverse" is used because we are navigating the relationship in the opposite direction—starting from the model that doesn't contain the ForeignKey field (Instructor) and accessing the model that does contain the ForeignKey field (Course).

```py
instructor = Instructor.objects.get(id=1)
for course in instructor.courses.all():
    print(course.title)

```

n this example, we are going from the Instructor model (which doesn't directly store any information about courses) and fetching all related Course objects via the reverse ForeignKey relationship.

#### When to Use prefetch_related with Reverse ForeignKey

When we have a reverse ForeignKey relationship and want to avoid the n+1 problem, we can use prefetch_related to load related objects efficiently.

```py
instructors = Instructor.objects.prefetch_related('courses')
for instructor in instructors:
    print(instructor.name)
    for course in instructor.courses.all():
        print(course.title)
```

This will issue 2 queries:

1. One query to get all instructors.
2. Another query to get all courses that belong to the fetched instructors, avoiding n+1 queries for each instructor.

## Caching

it is a layer between the django app and our database, if we implement caching, when the client makes a request, django first looks into our cache if the requested data is available, if not,then it will ask the databases to serve.

## Profiling

Profiling helps us measure how much time is spent on each part of our code or how many system resources (CPU, memory, etc.) are being used.

Profiling helps us pinpoint which specific parts of our code are slow or resource-heavy.

## Benchmarking

2. Benchmarking

Benchmarking is a technique to measure the overall performance of our application under various conditions. Unlike profiling (which focuses on code internals), benchmarking tests the application’s performance in terms of response times, throughput, and resource usage under load. It's usually done by simulating traffic or workload that our app would handle in production.

Benchmarking helps us assess how well our application performs under varying levels of load.

#### Key Metrics in Benchmarking:

Response Time (Latency): How long it takes for the application to respond to a request.
Throughput (Requests per second): The number of requests our application can handle per second.
CPU/Memory Usage: Measures the CPU and memory consumption under load.

```sh
ab -n 1000 -c 10 http://127.0.0.1:8000/
```

```table
### Profiling vs. Benchmarking

| **Feature**  | **Profiling**                                      | **Benchmarking**                                |
|--------------|----------------------------------------------------|-------------------------------------------------|
| **Focus**    | Individual code performance (time, memory, CPU)    | Overall system performance (latency, throughput) |
| **Usage**    | Analyze bottlenecks in code                        | Measure application performance under load      |
| **Tools**    | cProfile, django-silk, memory-profiler             | Apache Benchmark, Siege, Locust                 |
| **Goal**     | Optimize specific functions or queries             | Ensure the system can handle real-world traffic  |

```
