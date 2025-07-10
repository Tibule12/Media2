import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Stories from '../Stories.vue';

describe('Stories.vue', () => {
  it('renders stories container', () => {
    const wrapper = mount(Stories);
    expect(wrapper.exists()).toBe(true);
  });
});
