from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
    menu_show_home = False

    menu = (
        ParentItem('User Administration', children=[
            ChildItem('Users', model='auth.user'),
            ChildItem('Groups', model='auth.group')
        ], icon='fa fa-leaf'),

        ParentItem('Agents', children=[
            ChildItem(model='bpos_agents.agent')
        ], icon='fa fa-leaf'),

        ParentItem('Airports', children=[
            ChildItem(model='bpos_airports.airport')
        ], icon='fa fa-leaf'),

        ParentItem('Guides', children=[
            ChildItem(model='bpos_guides.guide')
        ], icon='fa fa-leaf'),

        ParentItem('Towns', children=[
            ChildItem(model='bpos_towns.town')
        ], icon='fa fa-leaf'),

        ParentItem('Hotels', children=[
            ChildItem(model='bpos_hotels.hotel')
        ], icon='fa fa-leaf'),

        ParentItem('Payment Items', children=[
            ChildItem('Payment Out Items', model='bpos_payment_out_items.paymentextraitems'),
            ChildItem('Extra Chargable Items', model='bpos_extra_items.extraitems')
        ], icon='fa fa-leaf'),

        ParentItem('Back To Site', url="/", icon='fa fa-leaf'),
    )

    def ready(self):
        super(SuitConfig, self).ready()
