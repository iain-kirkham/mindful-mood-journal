from django.test.runner import DiscoverRunner
from django.db import connections
from testcontainers.postgres import PostgresContainer
from django.db.backends.postgresql.creation import DatabaseCreation


class NoCreateDatabaseCreation(DatabaseCreation):
    def _create_test_db(self, verbosity, autoclobber, keepdb):
        return self.connection.settings_dict["NAME"]

    def _destroy_test_db(self, test_database_name, verbosity):
        pass


class TestContainerRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        self.postgres = PostgresContainer("postgres:15-alpine")
        self.postgres.start()

        db_host = self.postgres.get_container_host_ip()
        db_port = self.postgres.get_exposed_port(5432)
        db_user = self.postgres.username
        db_pass = self.postgres.password
        db_name = self.postgres.dbname

        container_creds = {
            "HOST": db_host,
            "PORT": db_port,
            "USER": db_user,
            "PASSWORD": db_pass,
            "NAME": db_name,
            "TEST": {
                "NAME": db_name,
                "MIRROR": None,
                "MIGRATE": True,
                "CHARSET": None,
                "COLLATION": None,
            },
        }

        for alias in connections:
            connections[alias].close()
            connections[alias].settings_dict.update(container_creds)
            connections[alias].creation = NoCreateDatabaseCreation(connections[alias])

        print(f"--- Container Active on {db_host}:{db_port} ---")
        return super().setup_databases(**kwargs)

    def teardown_databases(self, old_config, **kwargs):
        try:
            super().teardown_databases(old_config, **kwargs)
        finally:
            if hasattr(self, "postgres"):
                self.postgres.stop()
