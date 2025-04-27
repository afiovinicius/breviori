import strawberry

from src.app.api.resolvers.short import (
    Query as ShortQuery,
    Mutation as ShortMutation,
)


@strawberry.type
class Query(ShortQuery):
    pass


@strawberry.type
class Mutation(ShortMutation):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
