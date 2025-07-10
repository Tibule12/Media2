import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Welcome from '../Welcome.vue';

describe('Welcome.vue', () => {
  it('renders welcome container', () => {
    const wrapper = mount(Welcome);
    expect(wrapper.exists()).toBe(true);
  });
});
