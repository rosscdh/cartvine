# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Widget'
        db.create_table('widget_widget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('widget_type', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('data', self.gf('jsonfield.fields.JSONField')(default='{"templates": [""], "icons": {"widget_list": ""}}', null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('widget', ['Widget'])

        # Adding model 'WidgetInfo'
        db.create_table('widget_widgetinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['widget.Widget'])),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plan.Plan'])),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('widget', ['WidgetInfo'])

        # Adding model 'WidgetShop'
        db.create_table('widget_widget_shop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['widget.Widget'])),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Shop'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('data', self.gf('jsonfield.fields.JSONField')(default='{"target_id": "body"}', null=True)),
        ))
        db.send_create_signal('widget', ['WidgetShop'])


    def backwards(self, orm):
        # Deleting model 'Widget'
        db.delete_table('widget_widget')

        # Deleting model 'WidgetInfo'
        db.delete_table('widget_widgetinfo')

        # Deleting model 'WidgetShop'
        db.delete_table('widget_widget_shop')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'plan.plan': {
            'Meta': {'object_name': 'Plan'},
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'shop.shop': {
            'Meta': {'object_name': 'Shop'},
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'etag_updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['plan.Plan']"}),
            'provider_access_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'provider_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'db_index': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'widget.widget': {
            'Meta': {'ordering': "['name']", 'object_name': 'Widget'},
            'data': ('jsonfield.fields.JSONField', [], {'default': '\'{"templates": [""], "icons": {"widget_list": ""}}\'', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['plan.Plan']", 'through': "orm['widget.WidgetInfo']", 'symmetrical': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'shop': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['shop.Shop']", 'through': "orm['widget.WidgetShop']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'widget_type': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'widget.widgetinfo': {
            'Meta': {'ordering': "['widget__name', 'plan']", 'object_name': 'WidgetInfo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['plan.Plan']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['widget.Widget']"})
        },
        'widget.widgetshop': {
            'Meta': {'object_name': 'WidgetShop', 'db_table': "'widget_widget_shop'"},
            'data': ('jsonfield.fields.JSONField', [], {'default': '\'{"target_id": "body"}\'', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Shop']"}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['widget.Widget']"})
        }
    }

    complete_apps = ['widget']