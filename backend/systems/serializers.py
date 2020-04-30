# -*- coding: utf-8 -*-
# author: timor

from systems.models import *
from systems.menus import init_menu
from rest_framework import serializers


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        roles = validated_data.pop('roles')
        obj = User.objects.create(**validated_data)
        if len(roles) > 0:
            obj.roles.set(roles)
        else:
            role = Role.objects.get(id=1)
            obj.roles.add(role)
        try:
            obj.set_password(validated_data['password'])
        except:
            pass
        obj.save()
        return obj

    def update(self, instance, validated_data):
        roles = validated_data.pop('roles')
        instance.username = validated_data.get('username', instance.username)
        instance.realname = validated_data.get('realname', instance.realname)
        instance.group = validated_data.get('group', instance.group)
        instance.email = validated_data.get('email', instance.email)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.status = validated_data.get('status', instance.status)
        instance.memo = validated_data.get('memo', instance.memo)
        try:
            instance.set_password(validated_data['password'])
        except:
            pass
        instance.roles.set(roles)
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

    def create(self, validated_data):
        obj = Menu.objects.create(**validated_data)
        if obj.type == 2:
            init_menu(obj)
        return obj
