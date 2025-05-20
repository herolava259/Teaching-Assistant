
Generic single-database configuration.

data_base_url = postgresql+psycopg2://ghostofrace:1QAZ2wsx3EDC$@localhost/teachingassistantdb

## 1.Create migration

<pre>'''bash
alembic revision --autogenerate -m "update schema with my event/ description"
'''</pre>
### > After running above bash, it will generate a file migration at **./versions**

## 2.Run migration

<pre>'''bash
alembic upgrade head
'''</pre>

## 3. After some update schema
- When once day, you has some update schema on some table like, declare additional column, delete column, add constraint, index
You update on .../schema.py, so on you need update on database specially is postgresql. Therefore you should run the two above command
or like this

<pre>'''bash
alembic revision --autogenerate -m "add age column to users"
alembic upgrade head
'''</pre>


## 4. Some helpful Alembic commands

| Commands                          | Meaning                                      |
| --------------------------------- | ---------------------------------------------|
| `alembic init alembic`            | Create Alembic project                       |
| `alembic revision -m "msg"`       | Create migration manually                    |
| `alembic revision --autogenerate` | Create migration automatically from ORM model|
| `alembic upgrade head`            | Run all newest migrations                    |
| `alembic downgrade -1`            | Rollback previous migration one step         |
| `alembic history`                 | Read history of migrations                   |
| `alembic current`                 | Check current migration on database          |

