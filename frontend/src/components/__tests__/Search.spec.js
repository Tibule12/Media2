import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Search from '../Search.vue';

describe('Search.vue', () => {
  it('renders search container', () => {
    const wrapper = mount(Search);
    expect(wrapper.exists()).toBe(true);
  });
});
