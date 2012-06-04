# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Webhook'
        db.create_table('webhook_webhook', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Shop'])),
            ('provider_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('address', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('webhook', ['Webhook'])

        # Adding model 'OrderCreatePostback'
        db.create_table('webhook_ordercreatepostback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Shop'])),
            ('shop_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('date_recieved', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('recieved_from', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('recieved_from_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('data', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal('webhook', ['OrderCreatePostback'])


    def backwards(self, orm):
        # Deleting model 'Webhook'
        db.delete_table('webhook_webhook')

        # Deleting model 'OrderCreatePostback'
        db.delete_table('webhook_ordercreatepostback')


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
        'webhook.ordercreatepostback': {
            'Meta': {'ordering': "['-pk']", 'object_name': 'OrderCreatePostback'},
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {}),
            'date_recieved': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recieved_from': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'recieved_from_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Shop']"}),
            'shop_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'webhook.webhook': {
            'Meta': {'object_name': 'Webhook'},
            'address': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Shop']"}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['webhook']