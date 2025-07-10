import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import MainLayout from '../MainLayout.vue';

describe('MainLayout.vue', () => {
  it('renders main layout container', () => {
    const wrapper = mount(MainLayout);
    expect(wrapper.exists()).toBe(true);
  });
});
