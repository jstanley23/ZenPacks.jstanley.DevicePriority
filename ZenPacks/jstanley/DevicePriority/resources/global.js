(function () {

    /* Control zProperty values by using comboboxes */
    if (Zenoss.zproperties.registerZPropertyType) {
        Ext.define('Zenoss.form.zDevicePriorityBehavior.ComboBox', {
            alias: ['widget.zDevicePriorityBehavior-combobox'],
            extend: 'Ext.form.ComboBox',
            constructor: function(config) {
                config = config || {};

                Ext.applyIf(config, {
                    fieldLabel: _t('Behavior of device priority'),
                    name: 'zDevicePriorityBehavior',
                    editable: false,
                    forceSelection: true,
                    autoSelect: true,
                    triggerAction: 'all',
                    queryMode: 'local',
                    store: ['Adjust', 'Base', 'Default'],
                    listeners: {
                        select: function(combo, records) {
                            this.fireEvent('validitychange');
                        }
                    }
                });

                this.callParent(arguments);
            }
        });

        Ext.define('Zenoss.form.zDevicePriorityChangeSkip.ComboBox', {
            alias: ['widget.zDevicePriorityChangeSkip-combobox'],
            extend: 'Ext.form.ComboBox',
            constructor: function(config) {
                config = config || {};

                Ext.applyIf(config, {
                    fieldLabel: _t('Severity level to skip'),
                    name: 'zDevicePriorityChangeSkip',
                    editable: false,
                    forceSelection: true,
                    autoSelect: true,
                    triggerAction: 'all',
                    queryMode: 'local',
                    store: ['Info', 'Warning', 'Error', 'Critical'],
                    listeners: {
                        select: function(combo, records) {
                            this.fireEvent('validitychange');
                        }
                    }
                });

                this.callParent(arguments);
            }
        });

        Ext.define('Zenoss.form.zDevicePriorityEventTypes.ComboBox', {
            alias: ['widget.zDevicePriorityEventTypes-combobox'],
            extend: 'Ext.form.ComboBox',
            constructor: function(config) {
                config = config || {};

                Ext.applyIf(config, {
                    fieldLabel: _t('Event types to adjust'),
                    name: 'zDevicePriorityEventTypes',
                    editable: false,
                    forceSelection: true,
                    autoSelect: true,
                    triggerAction: 'all',
                    queryMode: 'local',
                    store: ['Ping Down', 'Windows Services', 'All', 'Custom'],
                    listeners: {
                        select: function(combo, records) {
                            this.fireEvent('validitychange');
                        }
                    }
                });

                this.callParent(arguments);
            }
        });

        
        Zenoss.zproperties.registerZPropertyType('zDevicePriorityBehavior', {
            'xtype': 'zDevicePriorityBehavior-combobox'
        });
        Zenoss.zproperties.registerZPropertyType('zDevicePriorityChangeSkip', {
            'xtype': 'zDevicePriorityChangeSkip-combobox'
        });
        Zenoss.zproperties.registerZPropertyType('zDevicePriorityEventTypes', {
            'xtype': 'zDevicePriorityEventTypes-combobox'
        });
        
    }

})();
